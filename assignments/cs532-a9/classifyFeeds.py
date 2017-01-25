import json
import os
import statistics
from collections import Counter,defaultdict

import feedparser
import requests
from feedgen.feed import FeedGenerator
from sklearn.cross_validation import KFold
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score,precision_score,recall_score
from tabulate import tabulate

import pygn
from docclass import *

fmeasure = "http://f-measure.blogspot.com/feeds/posts/default?max-results=200"
# regex to capture the self labeled topic of the blog post
findClass = re.compile("^.+\\((.+)\\)$")

# extract the artist portion. Capture everything until our negative look ahead says we have a space - space "
artistsExtractor = re.compile("^(?!\s\-\s\")([a-zA-Z0-9.&\-']+\s(?:[a-zA-Z0-9.&\-']+\s)*)")

# Gracenote Music Web API user id
# used for pygen in order to get the genre of the artits
gnmUID = "put yours here"


def check_next(text):
    # check for the next button ie pagination of blog pages
    soup = BeautifulSoup(text, "lxml-xml")
    next_page = soup.find_all('link', attrs={'type': 'application/atom+xml', 'rel': 'next'})
    # if there is a next page our next_page list will always be 1 otherwise its 0
    # that means we have consumed all the pages for the blog
    if len(next_page) > 0:
        nl = next_page[0].attrs['href']
        return True, nl
    return False, None


def getDataFeed():
    # have a useragent so we do not look like a robot
    useragent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
    sesh = requests.Session()  # type: requests.Session
    sesh.headers.update({'User-Agent': useragent})
    r = sesh.get(fmeasure)
    # ok to make the gotten feed slimmer I will be building a new one
    # containing only the title of the blog, the feed it
    # and the entries so I am using feedgen library to do so
    fg = FeedGenerator()
    feed = feedparser.parse(r.text)
    fg.title(feed.feed.title)
    fg.id(feed.feed.id)
    entries = []
    # concatenate every entry from the current pagination
    entries.extend(feed.entries)
    # as usual check next and while good get next set of entries
    # and extract the entries
    good, nl = check_next(r.text)
    while good:
        r = sesh.get(nl)
        feed = feedparser.parse(r.text)
        entries.extend(feed.entries)
        good, nl = check_next(r.text)
        r.close()
    # for each of the entries
    for e in entries:
        # create a new entry
        fe = fg.add_entry()
        # add the entry id, title and content
        fe.id(e.id)
        fe.title(e.title)
        c = e.content[0]
        fe.content(content=c.value, type=c.type)
    # write the new feed file out
    fg.atom_file("datafiles/f-measure.xml", pretty=True)
    sesh.close()
    # now to get the genres
    get_genres()


def genre_sanity(it):
    '''
    This method is a quick overview of how
    I reduce genres down to a single one
    Yes its a mess but hey
    '''
    if "New Wave" in it:
        return "Indie Rock/Alternative"
    if "Indie Rock" in it:
        return "Indie Rock/Alternative"
    if "Punk" in it:
        return "Metal/Punk/Hardcore"
    if "Rock" in it:
        return "Rock"
    if "Pop" in it:
        return "Pop/Electronic/Hip-Hop"
    if "Techno" in it or "Electronica" in it \
            or "Intelligent (IDM)" in it or "Downtempo, Lounge & Ambient" in it \
            or "Trip Hop" in it:
        return "Pop/Electronic/Hip-Hop"
    if "Electronic" in it:
        return "Pop/Electronic/Hip-Hop"
    if "Metal" in it:
        return "Metal/Punk/Hardcore"
    if "Emo" in it or "Hardcore" in it:
        return "Metal/Punk/Hardcore"
    if "Hip-Hop" in it:
        return "Pop/Electronic/Hip-Hop"
    if "Country" in it or "Comedy" in it or "Classical" in it or "Americana" in it:
        return "R&B/Jazz/Mowtown/Country/Other"
    if "R&B" in it or "Jazz" in it or "Mowtown" in it or "Soul" in it \
            or "Reggae" in it or "Ska" in it or "Urban" in it or "Funk" in it:
        return "R&B/Jazz/Mowtown/Country/Other"
    if "Lo-Fi" in it or "Shoegazer" in it or "Slowcore" in it or "Neo-Psychedelic" in it or "Alternative" in it:
        return "Indie Rock/Alternative"
    if "Classic Prog" in it:
        return "Rock"
    if "Post-Modern Art" in it or "Bakersfield Sound":
        return "R&B/Jazz/Mowtown/Country/Other"
    return it


def determine_genre(artist, genreList):
    # The genre is the first one in the list as it is the dominate one
    # I denote the first genre in the list as dominate as it is the most relevant
    # if the list is empty say none
    genre = genreList[0] if len(genreList) != 0 else None
    # this portion I by hand say what genre an artist is
    # they have David Bowie as Glam technically yes
    # he is fabulous but seriously Rock
    if "My Bloody Valentine" in artist:
        return "Metal/Punk/Hardcore"
    if "Ultravox" in artist:
        return "Rock"
    if "DJ Shadow" in artist:
        return "Pop/Electronic/Hip-Hop"
    if "David Bowie" in artist:
        return "Rock"
    if genre is None:
        # genre is none happens sometime for the various artists blog entries
        # but I know these artists happen with it
        # otherwise I do not know how to classify the genre so default
        if "The Nerves" in artist:
            return "Rock"
        if "Blacktask" in artist:
            return "Metal/Punk/Hardcore"
        return "R&B/Jazz/Mowtown/Country/Other"
    # sanitize the genre after everything
    return genre_sanity(genre)


def get_genres():
    # read the newly created feed
    feed = feedparser.parse("datafiles/f-measure.xml")

    # want the set of unique artists
    uniqueArtists = set()

    # get the artists from the feed
    for e in feed.entries:
        m = artistsExtractor.match(e.title)
        if m is not None:
            # my regex grabs the trailing space dash in some cases
            # so remove it
            uniqueArtists.add(m.group(1).rstrip(" -"))
    # set up for getting the unique artist genre
    userID = pygn.register(gnmUID)
    artistsInfo = {}  # store all associated genre information per artist
    artistsToGenre = {}  # store the direct mapping of the chosen genre
    # for each artist
    for ua in uniqueArtists:
        # get their metadata
        metaData = pygn.search(clientID=gnmUID, userID=userID, artist=ua)
        uaG = []
        print(ua)
        # if its not none then Gracenote Music has information on them
        if metaData is not None:
            # extract the genre for the artists
            for genre in map(lambda ge: ge['TEXT'], metaData['genre'].values()):
                uaG.append(genre)
        artistsInfo[ua] = uaG
        artistsToGenre[ua] = determine_genre(ua, uaG)
    # write data to file
    with open("datafiles/artistsInfo.json", "w+") as out:
        out.write(json.dumps(artistsInfo, indent=1))
    with open("datafiles/artistsToGenre.json", "w+") as out:
        out.write(json.dumps(artistsToGenre, indent=1))


def labelCounter():
    # I want to be able to know what how many labels i have
    # for reporting and sanity checking
    # load the artist genre information
    with open("datafiles/artistsInfo.json", "r") as ai:
        artistsData = json.load(ai)
    gCounter = Counter()
    artistsToGenre = {}
    # count genre and map it to artist
    for artist, genres in sorted(artistsData.items(), key=lambda x: x[0]):
        genre = determine_genre(artist, genres)
        gCounter[genre] += 1
        print(artist, genre, genres)
        artistsToGenre[artist] = genre
        print("--------------------------------------")

    genreToEntry = defaultdict(list)
    feed = feedparser.parse("datafiles/f-measure.xml")
    gc = Counter()
    gcc = 0
    # count number of genres for all feed entries
    # and find out which genres we are training on
    for e in feed.entries:
        m = artistsExtractor.match(e.title)
        g = None
        if m is not None:
            art = m.group(1).rstrip(" -")
            genreToEntry[artistsToGenre[art]].append(e)
            g = artistsToGenre[art]
        else:
            genreToEntry["R&B/Jazz/Mowtown/Country/Other"].append(e)
            g = "R&B/Jazz/Mowtown/Country/Other"
        if gcc < 50:
            gc[g] += 1
            gcc += 1

    print(gc)
    fgl = []
    fcl = []
    # for the first 50 training items table
    for fg, fc in gc.items():
        fgl.append(fg)
        fcl.append(fc)

    with open("datafiles/genreFirst50LatexTable.txt", "w+") as lout:
        lout.write(tabulate({"class": fgl, "classCount": fcl}, headers="keys", tablefmt="latex"))

    # for all items
    genrel = []
    genrecl = []
    for g, gl in genreToEntry.items():
        print(g, len(gl))
        genrel.append(g)
        genrecl.append(len(gl))

    with open("datafiles/genreAllLatexTable.txt", "w+") as lout:
        lout.write(tabulate({"class": genrel, "classCount": genrecl}, headers="keys", tablefmt="latex"))

    # my original labels reporting section
    oToE = defaultdict(list)
    count = 0
    cc = Counter()

    for e2 in feed.entries:
        clazz = findClass.match(e2.title).group(1).lower().strip()
        if "concert" in clazz or 'spotlight' in clazz:
            clazz = 'concert/spotlight'
        oToE[clazz].append(e2)
        if count < 50:
            cc[clazz] += 1
            count += 1
    print("------------------------------")
    print(cc)

    fl = []
    cl = []
    for fg, fc in cc.items():
        fl.append(fg)
        cl.append(fc)

    with open("datafiles/allFirst50RegLatexTable.txt", "w+") as lout:
        lout.write(tabulate({"class": fl, "classCount": cl}, headers="keys", tablefmt="latex"))

    clzzl = []
    clzzcl = []
    for clzz, cl in oToE.items():
        print(clzz, len(cl))
        clzzl.append(clzz)
        clzzcl.append(len(cl))

    with open("datafiles/allRegLatexTable.txt", "w+") as lout:
        lout.write(tabulate({"class": clzzl, "classCount": clzzcl}, headers="keys", tablefmt="latex"))


def do_classification(dbfile, startStop=(50, 100), extension=False):

    # This is the original label classification method
    # dbfile: the database file to be used
    # startStop: are we doing the first 100 or all data,start train on count,stop is classification
    # extension: are we doing using the extension for features
    # parse the feed and create the classifier
    feed = feedparser.parse("datafiles/f-measure.xml")
    if extension:
        cl = fisherclassifier(dbfile, getfeatures=entryfeatures)
    else:
        cl = fisherclassifier(dbfile)
    # counter for training data
    trainCount = 0
    # for reporting
    labs = ['forgotten song', 'concert/spotlight', 'lp review', 'the song remains the same']
    actualLabels = []
    predictedLabels = []
    tabelOut = defaultdict(list)
    trainedOut = defaultdict(list)

    # I do not ask the user for a label as I let the structure of the blog be the user specified aspect
    # ie Merle Haggard - "Mama Tried" (forgotten song): forgotten song is the label/category
    for e in feed.entries:
        print("-----------------------------------")
        # get the label
        clazz = findClass.match(e.title).group(1).lower().strip()
        # I combine concert and spotlight into a combined label
        if "concert" in clazz or 'spotlight' in clazz:
            clazz = 'concert/spotlight'
        # get the data to be used depending on if we are using the extension or not
        text = "%s\n%s" % (e.title, BeautifulSoup(e.summary, "html5lib").text) if not extension else e
        # since train count starts at zero like any good cs person we
        if trainCount < startStop[0]:
            # train and log what we trained
            cl.train(text, clazz)
            print("Training iteration %d for entry title: %s with class %s" % (trainCount, e.title, clazz))
            trainedOut['Title'].append(e.title)
            trainedOut['Category'].append(clazz)
            print("--------------------------------------------------")
            trainCount += 1
        else:
            # now we classify
            if startStop[0] <= trainCount < startStop[1]:
                print("Classify iteration %d for entry title: %s with class %s" % (trainCount, e.title, clazz))
                # classify and store data for reporting
                prediction = cl.classify(text, "indeterminable")
                actualLabels.append(clazz)
                predictedLabels.append(prediction)
                cprob = cl.cprobLast
                fprob = cl.fisherprob(text, clazz)
                tabelOut['title'].append(e.title)
                tabelOut['predicted_cat'].append(prediction)
                tabelOut['actual_cat'].append(clazz)
                tabelOut['acat_fprob'].append(fprob)
                os = "Title: %s, predcat: %s, actcat: %s, acat_cprob: %f, acat_fprob: %f" % (
                    e.title, prediction, clazz, cprob, fprob)
                print(os)
                print("--------------------------------------------------")
                trainCount += 1

    # our file names are dependent on if we are using 100 entries or all of them
    if startStop[1] == 100:
        ctable = "tables/regClassificationTable.txt" if not extension else "tables/regClassificationTable-e.txt"
        creport = "reports/regClassificationReport.txt" if not extension else \
            "reports/regClassificationReport-e.txt"
        train = "tables/regTrainTable.txt" if not extension else "tables/regTrainTable-e.txt"
    else:
        ctable = "tables/regClassificationTableAll.txt" if not extension else \
            "tables/regClassificationTableAll-e.txt"
        creport = "reports/regClassificationReportAll.txt" if not extension else \
            "reports/regClassificationReportAll-e.txt"
        train = "tables/regTrainTableAll.txt" if not extension else "tables/regTrainTableAll-e.txt"

    # write out information
    with open(ctable, "w+") as tout:
        tout.write(tabulate(tabelOut, headers="keys", tablefmt="latex"))

    with open(creport, "w+") as rout:
        rout.write(classification_report(actualLabels, predictedLabels, labels=labs, target_names=labs))

    with open(train, "w+") as tout:
        tout.write(tabulate(trainedOut, headers="keys", tablefmt="latex"))
    cl.close_con()


def myTest(dbfile, startStop=(50, 100), extension=False):
    # works the same as the first one but we are classifying on genre
    with open("datafiles/artistsToGenre.json", "r") as agi:
        aTg = json.load(agi)
    feed = feedparser.parse("datafiles/f-measure.xml")
    labs = ['Rock', 'R&B/Jazz/Mowtown/Country/Other', 'Metal/Punk/Hardcore', 'Indie Rock/Alternative',
            'Pop/Electronic/Hip-Hop']
    if extension:
        cl = fisherclassifier(dbfile, getfeatures=entryfeatures)
    else:
        cl = fisherclassifier(dbfile)
    actualLabels = []
    predictedLabels = []
    tabelOut = defaultdict(list)
    trainedOut = defaultdict(list)
    trainCount = 0
    for e in feed.entries:
        m = artistsExtractor.match(e.title)
        if m is not None:
            clazz = aTg[m.group(1).rstrip(" -")]
        else:
            clazz = "R&B/Jazz/Mowtown/Country/Other"

        text = "%s\n%s" % (e.title, BeautifulSoup(e.summary, "html5lib").text) if not extension else e
        if trainCount < startStop[0]:
            cl.train(text, clazz)
            print("Training iteration %d for entry title: %s with class %s" % (trainCount, e.title, clazz))
            trainedOut['Title'].append(e.title)
            trainedOut['Category'].append(clazz)
            print("--------------------------------------------------")
            trainCount += 1
        else:
            if startStop[0] <= trainCount < startStop[1]:
                print("Classify iteration %d for entry title: %s with class %s" % (trainCount, e.title, clazz))
                prediction = cl.classify(text, "indeterminable")
                actualLabels.append(clazz)
                predictedLabels.append(prediction)
                cprob = cl.cprobLast
                fprob = cl.fisherprob(text, clazz)
                tabelOut['title'].append(e.title)
                tabelOut['predicted_cat'].append(prediction)
                tabelOut['actual_cat'].append(clazz)
                tabelOut['acat_fprob'].append(fprob)
                os = "Title: %s, predcat: %s, actcat: %s, acat_cprob: %f, acat_fprob: %f" % (
                    e.title, prediction, clazz, cprob, fprob)
                print(os)
                print("--------------------------------------------------")
                trainCount += 1

    if startStop[1] == 100:
        ctable = "tables/myTestClassificationTable.txt" if not extension else \
            "tables/myTestClassificationTable-e.txt"
        creport = "reports/myTestClassificationReport.txt" if not extension else \
            "reports/myTestClassificationReport-e.txt"
        train = "tables/myTestTrainTable.txt" if not extension else "tables/myTestTrainTable-e.txt"
    else:
        ctable = "tables/myTestClassificationTableAll.txt" if not extension else \
            "tables/myTestClassificationTableAll-e.txt"
        creport = "reports/myTestClassificationReportAll.txt" if not extension else \
            "reports/myTestClassificationReportAll-e.txt"
        train = "tables/myTestTrainTableAll.txt" if not extension else "tables/myTestTrainTableAll-e.txt"

    with open(ctable, "w+") as tout:
        tout.write(tabulate(tabelOut, headers="keys", tablefmt="latex"))

    with open(creport, "w+") as rout:
        rout.write(classification_report(actualLabels, predictedLabels, labels=labs, target_names=labs))

    with open(train, "w+") as tout:
        tout.write(tabulate(trainedOut, headers="keys", tablefmt="latex"))
    cl.close_con()


def tf_train(cl, clmt, kf, aTg, feed, fname):
    # ten fold cross validation method
    # kfold metric scores for the blog structure classification
    kfhMetrics = defaultdict(list)
    # kfold metric scores for genre classification
    kfhMetricsmt = defaultdict(list)
    # output tables
    tabelOut = defaultdict(list)
    tabelOut2 = defaultdict(list)
    count = 0
    # loop through the validation indexes
    for train_index, test_index in kf:
        # labels for output for structure and genre predictions
        actualLabels = []
        predictedLabels = []
        actualLabels2 = []
        predictedLabels2 = []
        print("Training for k=%d for %s" % (count + 1, fname))
        # train
        for i in train_index:
            # var1 is for the structure and var2 is for genre
            clazz1 = findClass.match(feed[i].title).group(1).lower().strip()
            if "concert" in clazz1 or 'spotlight' in clazz1:
                clazz1 = 'concert/spotlight'
            text1 = "%s\n%s" % (feed[i].title, BeautifulSoup(feed[i].summary, "html5lib").text)
            m = artistsExtractor.match(feed[i].title)
            if m is not None:
                clazz2 = aTg[m.group(1).rstrip(" -")]
            else:
                clazz2 = "R&B/Jazz/Mowtown/Country/Other"
            text2 = "%s\n%s" % (feed[1].title, BeautifulSoup(feed[1].summary, "html5lib").text)
            cl.train(text1, clazz1)
            clmt.train(text2, clazz2)
        print("Classifying for k=%d for %s" % (count + 1, fname))
        # classify
        for i in test_index:
            clazz1 = findClass.match(feed[i].title).group(1).lower().strip()
            if "concert" in clazz1 or 'spotlight' in clazz1:
                clazz1 = 'concert/spotlight'
            text1 = "%s\n%s" % (feed[i].title, BeautifulSoup(feed[i].summary, "html5lib").text)
            m = artistsExtractor.match(feed[i].title)
            if m is not None:
                clazz2 = aTg[m.group(1).rstrip(" -")]
            else:
                clazz2 = "R&B/Jazz/Mowtown/Country/Other"
            text2 = "%s\n%s" % (feed[i].title, BeautifulSoup(feed[i].summary, "html5lib").text)
            prediction = cl.classify(text1, "indeterminable")
            actualLabels.append(clazz1)
            predictedLabels.append(prediction)
            fprob = cl.fisherprob(text1, clazz1)

            tabelOut['title'].append(feed[i].title)
            tabelOut['predicted_cat'].append(prediction)
            tabelOut['actual_cat'].append(clazz1)
            tabelOut['acat_fprob'].append(fprob)
            prediction2 = clmt.classify(text2, "indeterminable")
            actualLabels2.append(clazz2)
            predictedLabels2.append(prediction2)
            fprob2 = clmt.fisherprob(text2, clazz2)
            tabelOut2['title'].append(feed[i].title)
            tabelOut2['predicted_cat'].append(prediction2)
            tabelOut2['actual_cat'].append(clazz2)
            tabelOut2['acat_fprob'].append(fprob2)
            # take mean of the values as the scikit learn scores returns the values for each label
            kfhMetrics['precision'].append(
                statistics.mean(precision_score(actualLabels, predictedLabels, average=None)))
            kfhMetrics['recall'].append(statistics.mean(recall_score(actualLabels, predictedLabels, average=None)))
            kfhMetrics['f1'].append(statistics.mean(f1_score(actualLabels, predictedLabels, average=None)))
            kfhMetricsmt['precision'].append(
                statistics.mean(precision_score(actualLabels2, predictedLabels2, average=None)))
            kfhMetricsmt['recall'].append(statistics.mean(recall_score(actualLabels2, predictedLabels2, average=None)))
            kfhMetricsmt['f1'].append(statistics.mean(f1_score(actualLabels2, predictedLabels2, average=None)))
        count += 1
        # you gotta do it from scratch k times
        cl.clear_db()
        clmt.clear_db()
    ret1 = []
    ret2 = []
    headers = ["metric", "mean"]
    for m, v in kfhMetrics.items():
        ret1.append([m, statistics.mean(v)])
    for m, v in kfhMetricsmt.items():
        ret2.append([m, statistics.mean(v)])

    print(ret1)
    print(ret2)

    with open("tables/tenfold-classret-%s.txt" % fname, "w+") as out:
        out.write(tabulate(tabelOut, headers="keys", tablefmt="latex"))
    with open("tables/tenfold-classret-mytest-%s.txt" % fname, "w+") as out:
        out.write(tabulate(tabelOut2, headers="keys", tablefmt="latex"))

    with open("tables/tenfold-metrics-%s.txt" % fname, "w+") as out:
        out.write(tabulate(ret1, headers=headers, tablefmt="latex"))
    with open("tables/tenfold-metrics-mytest-%s.txt" % fname, "w+") as out:
        out.write(tabulate(ret2, headers=headers, tablefmt="latex"))
    cl.close_con()
    clmt.close_con()


def ten_fold():
    # do the ten fold validation
    feed = feedparser.parse("datafiles/f-measure.xml")

    with open("datafiles/artistsToGenre.json", "r") as agi:
        aTg = json.load(agi)
    # feall is for all data and fehundo is for the original test
    feall = []
    fehundo = []

    count = 0
    for e in feed.entries:
        feall.append(e)
        if count < 100:
            fehundo.append(e)
            count += 1

    # create kfold index objects
    # the take the length of the data and the number of folds
    kfh = KFold(len(fehundo), 10)
    kfa = KFold(len(feall), 10)
    # create the classifiers
    cl = fisherclassifier("dbs/fmeasure10f.sqlite3")
    clmt = fisherclassifier("dbs/fmeasure-myTest10f.sqlite3")
    cl2 = fisherclassifier("dbs/fmeasure10f-all.sqlite3")
    clmt2 = fisherclassifier("dbs/fmeasure-myTest10f-all.sqlite3")
    tf_train(cl, clmt, kfh, aTg, fehundo, "hundred")
    tf_train(cl2, clmt2, kfa, aTg, feall, "all")


if __name__ == "__main__":
    cwd = os.getcwd()
    feedFile = "datafiles/f-measure.xml"
    if not os.path.exists("%s/datafiles" % cwd):
        os.makedirs("%s/datafiles" % cwd)
    if not os.path.exists("%s/datafiles/f-measure.xml" % cwd):
        getDataFeed()
        labelCounter()

    do_classification("dbs/fmeasure.sqlite3")
    myTest("dbs/fmeasure-myTest.sqlite3")

    do_classification("dbs/fmeasure-all.sqlite3", startStop=(98, 1000))
    myTest("dbs/fmeasure-myTest-all.sqlite3", startStop=(98, 1000))

    do_classification("dbs/fmeasure-extension.sqlite3", extension=True)
    myTest("dbs/fmeasure-myTest-extension.sqlite3", extension=True)

    do_classification("dbs/fmeasure-all-extension.sqlite3", startStop=(98, 1000), extension=True)
    myTest("dbs/fmeasure-myTest-all-extension.sqlite3", startStop=(98, 1000), extension=True)
    ten_fold()
