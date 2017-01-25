import math
import re
from sqlite3 import dbapi2 as sqlite

import nltk
from bs4 import BeautifulSoup


def getwords(doc):
    splitter = re.compile('\\W*')
    # print doc
    ## Remove all the HTML tags
    doc = re.compile(r'<[^>]+>').sub('', doc)
    # Split the words by non-alpha characters
    words = [s.lower().replace('\'', '') for s in nltk.word_tokenize(doc)
             if len(s) > 2 and len(s) < 20]

    # Return the unique set of words only
    return dict([(w, 1) for w in words])


def entryfeatures(entry):
    splitter = re.compile('\\W*')
    f = {}
    titlewords = []
    for s in nltk.word_tokenize(entry.title):
        if 2 < len(s) < 20:
            titlewords.append(s.lower().replace('\'', ''))

    for w in titlewords: f['Title:' + w] = 1
    # Extract the summary words
    summarywords = [s.lower().replace('\'', '') for s in
                    nltk.word_tokenize(BeautifulSoup(entry.summary, "html5lib").text)
                    if len(s) > 2 and len(s) < 20]

    # Count uppercase words
    uc = 0
    for i in range(len(summarywords)):
        w = summarywords[i]
        f[w] = 1
        if w.isupper(): uc += 1

        # Get word pairs in summary as features
        if i < len(summarywords) - 1:
            twowords = ' '.join(summarywords[i:i + 1])
            f[twowords] = 1

    # Keep creator and publisher whole
    # f['Publisher:'+entry['publisher']]=1

    # UPPERCASE is a virtual word flagging too much shouting
    if float(uc) / len(summarywords) > 0.3: f['UPPERCASE'] = 1

    return f


class classifier:
    def __init__(self, dbfile, getfeatures=getwords):
        self.fc = {}
        self.cc = {}
        self.getfeatures = getfeatures
        # i moved the connection of the database here
        # and we now have a set up
        self.con = sqlite.connect(dbfile)
        self.queries = {}
        self._setupDB()

    def _setupDB(self):
        # build database and read in our queries
        with open("datafiles/dbschema.sql", "r") as read:
            self.con.executescript(read.read())
        with open("datafiles/queries.txt", "r") as query:
            for line in map(lambda x: x.rstrip("\n").split(':'), query):
                self.queries[line[0]] = line[1]

    def manualClassdb(self, num, entry, feature, predicted, actual):
        self.con.execute(self.queries['classEntry']
                         % (num, entry, feature, predicted, actual, None))
        self.con.commit()

    def autoClassdb(self, num, entry, feature, predicted, actual, cp):
        self.con.execute(self.queries['classEntry']
                         % (num, entry, feature, predicted, actual, cp))
        self.con.commit()


    def incf(self, f, cat):
        count = self.fcount(f, cat)
        if count == 0:
            self.con.execute(self.queries['insert_newFeature']
                             % (f, cat))
        else:
            self.con.execute(
                self.queries['increment_feature']
                % (count + 1, f, cat))


    def fcount(self, f, cat):
        query = self.queries['count_Feature'] % (f, cat)
        res = self.con.execute(query).fetchone()
        if res is None:
            return 0
        else:
            return int(res[0])


    def incc(self, cat):
        count = self.catcount(cat)
        if count == 0:
            self.con.execute(self.queries['insert_cat'] % cat)
        else:
            self.con.execute(self.queries['increment_cat'] % (count + 1, cat))



    def catcount(self, cat):
        res = self.con.execute(self.queries['count_cat'] % cat).fetchone()
        if res is None:
            return 0
        else:
            return int(res[0])


    def categories(self):
        cur = self.con.execute(self.queries['get_cat'])
        return [d[0] for d in cur]


    def totalcount(self):
        res = self.con.execute(self.queries['total_cat_count']).fetchone()
        if res is None: return 0
        return res[0]

    def train(self, item, cat):
        features = self.getfeatures(item)
        for f in features:
            self.incf(f, cat)
        self.incc(cat)
        self.con.commit()

    def fprob(self, f, cat):
        if self.catcount(cat) == 0: return 0
        return self.fcount(f, cat) / self.catcount(cat)

    def weightedprob(self, f, cat, prf, weight=1.0, ap=0.5):
        basicprob = prf(f, cat)

        # Count the number of times this feature has appeared in
        # all categories
        totals = sum([self.fcount(f, c) for c in self.categories()])

        # Calculate the weighted average
        bp = ((weight * ap) + (totals * basicprob)) / (weight + totals)
        return bp

    def clear_db(self):
        self.con.execute("DELETE FROM feature_count")
        self.con.commit()
        self.con.execute("DELETE FROM category_count")
        self.con.commit()

    def close_con(self):
        self.con.commit()
        self.con.close()


class naivebayes(classifier):
    def __init__(self, dbfile, getfeatures=getwords):
        classifier.__init__(self, dbfile, getfeatures)
        self.thresholds = {}

    def docprob(self, item, cat):
        features = self.getfeatures(item)
        p = 1
        for f in features: p *= self.weightedprob(f, cat, self.fprob)
        return p

    def prob(self, item, cat):
        catprob = self.catcount(cat) / self.totalcount()
        docprob = self.docprob(item, cat)
        return docprob * catprob

    def setthreshold(self, cat, t):
        self.thresholds[cat] = t

    def getthreshold(self, cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]

    def classify(self, item, default=None):
        probs = {}
        max = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max:
                max = probs[cat]
                best = cat

        for cat in probs:
            if cat == best: continue
            if probs[cat] * self.getthreshold(best) > probs[best]: return default
        return best


class fisherclassifier(classifier):
    def __init__(self, dbfile, getfeatures=getwords):
        classifier.__init__(self, dbfile, getfeatures)
        self.minimums = {}
        self.cprobLast = 0.0
        self.fprobLast = 0.0

    def cprob(self, f, cat):
        # The frequency of this feature in this category
        clf = self.fprob(f, cat)
        if clf == 0: return 0

        # The frequency of this feature in all the categories
        freqsum = sum([self.fprob(f, c) for c in self.categories()])

        # The probability is the frequency in this category divided by
        # the overall frequency
        p = clf / freqsum

        self.cprobLast = p

        return p

    def fisherprob(self, item, cat):
        # Multiply all the probabilities together
        p = 1
        features = self.getfeatures(item)
        for f in features:
            p *= (self.weightedprob(f, cat, self.cprob))
        # Take the natural log and multiply by -2
        # I added this because we get a zero here in 10 fold
        try:
            fscore = -2 * math.log(p)
        except ValueError:
            fscore = -2 * math.log(self.fprobLast)
        self.fprobLast = fscore
        # Use the inverse chi2 function to get a probability
        return self.invchi2(fscore, len(features) * 2)

    def invchi2(self, chi, df):
        m = chi / 2.0
        sum = term = math.exp(-m)
        for i in range(1, df // 2):
            term *= m / i
            sum += term
        return min(sum, 1.0)

    def setminimum(self, cat, min):
        self.minimums[cat] = min

    def getminimum(self, cat):
        if cat not in self.minimums: return 0
        return self.minimums[cat]

    def classify(self, item, default=None):
        # Loop through looking for the best result
        best = default
        max = 0.0
        for c in self.categories():
            p = self.fisherprob(item, c)
            # Make sure it exceeds its minimum
            if p > self.getminimum(c) and p > max:
                best = c
                max = p
        return best
