import re
from collections import defaultdict
from operator import add
import feedparser
import nltk
from bs4 import BeautifulSoup
from functional import seq
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
import json as jjson

removeExtra = re.compile('[^a-zA-Z]')
stop = stopwords.words('english')


def getwords(doc):
    splitter = re.compile('\\W*')
    # print doc
    ## Remove all the HTML tags
    doc = re.compile(r'<[^>]+>').sub('', doc)
    # Split the words by non-alpha characters
    words = [s.lower().replace('\'', '') for s in nltk.word_tokenize(doc)
             if len(s) > 2 and len(s) < 20]
    words = seq(words ).map(lambda word: (word, 1)) \
        .reduce_by_key(add) \
        .order_by(lambda x: x[1]).to_dict()
    # Return the unique set of words only
    return dict([(w, 1) for w in words])

# modified process text
def process_text(text):
    # clean text
    t = removeExtra.sub(' ', BeautifulSoup(text.content[0].value, 'html5lib').text).lower()
    ret = []
    # tokenize according to word and emit word if it is not a stopword
    for word in nltk.word_tokenize(t):
        if len(word) > 2:
            ret.append(word)
    ret = seq(ret).map(lambda word: (word, 1)) \
        .reduce_by_key(add) \
        .order_by(lambda x: x[1]).to_dict()
    return {'title': text.title, 'text': ret}

# modified consume all since
def consume_all(fileName):
    def foldHelp(acum,v):
        acum[v['title']] = v['text']
        return acum
    with open("datafiles/fmeasure.json","w+") as out:
        out.write(jjson.dumps(seq(feedparser.parse(fileName).entries).map(process_text).fold_left({},foldHelp),indent=1))

    with open("datafiles/inorder.txt","w+") as out:
        seq(feedparser.parse(fileName).entries).map(lambda e: out.write("%s\n"%e.title)).to_list()

# this class represents the word data for a particular feed
class feed:
    # pass flag if we are to do the stemming
    def __init__(self, fentry, doStem=False):
        self.title = fentry[0]
        self.wordCount = fentry[1]
        self.stemCount = defaultdict(int)
        if doStem:
            self._stem_count()

    def _stem_count(self):
        eng = EnglishStemmer()
        for word in self.wordCount.keys():
            self.stemCount[eng.stem(word)] += 1

    def words(self):
        return set(self.wordCount.keys())

    def __str__(self):
        return "%s: %s" % (self.title, ' '.join(list(self.wordCount.keys())))


# fake tfidf
def filter_fun(wc):
    frac = float(wc[1]) / float(100)
    return 0.1 < frac < 0.5


# output for the non-stemmed data file
def output(f, top):
    out = [f.title]
    for wd in top:
        out.append("%d" % f.wordCount.get(wd, 0))
    return '\t'.join(out) + "\n"


# output for the stemmed data file
def output_stem(f, top):
    out = [f.title]
    for wd in top:
        out.append("%d" % f.stemCount.get(wd, 0))
    return '\t'.join(out) + "\n"


def generate_blogfile():
    # read the data in as json and then transform to feeds
    feedData = seq.json("datafiles/fmeasure.json").map(lambda fe: feed(fe)).to_list()  # type: list[feed]
    '''
    get the top 500 words by word count over all words:
        for feed <- feeds, (word,count) <- feed.wordCount.items(): yeild (word,count)
        keep all wordCounts > 10
        groupby + reduce word:(word1,c1),(word1,c2) -> (word1,c1,c2,c3,c4) -> (word1,sumC)
        keep all wordCounts that meet fake tfidf
        transform (word,sumC) -> word
        take top 500
        transform to list
    '''
    top500 = seq(feedData).flat_map(lambda f: list(f.wordCount.items())) \
        .map(lambda wc: (wc[0], wc[1])) \
        .reduce_by_key(add) \
        .filter(filter_fun) \
        .order_by(lambda wc: -wc[1]) \
        .map(lambda wc: wc[0]) \
        .to_list()
    # sort alphabetically
    top500 = sorted(top500)
    print(len(top500))
    # write resultant to file
    with open("datafiles/fmeasure.txt", "w+") as out:
        out.write("Blog\t%s\n" % '\t'.join(top500))
        for tf in sorted(feedData, key=lambda f: f.title):
            out.write(output(tf, top500))


def generate_blogfile_stem():
    # same as non-stem except use stemmed data
    feedData = seq.json("datafiles/fmeasure.json").map(lambda fe: feed(fe, True)).to_list()  # type: list[feed]
    top500 = seq(feedData).flat_map(lambda f: list(f.stemCount.items())) \
        .map(lambda wc: (wc[0], wc[1])) \
        .reduce_by_key(add) \
        .filter(filter_fun) \
        .order_by(lambda wc: -wc[1]) \
        .map(lambda wc: wc[0]) \
        .to_list()
    top500 = sorted(top500)
    print(len(top500))
    with open("datafiles/fmeasure_stemmed.txt", "w+") as out:
        out.write("Blog\t%s\n" % '\t'.join(top500))
        for tf in sorted(feedData, key=lambda f: f.title):
            out.write(output_stem(tf, top500))
