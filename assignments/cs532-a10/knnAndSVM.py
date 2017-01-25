import json
import re
import statistics
from collections import defaultdict

from sklearn.cross_validation import KFold
from sklearn.metrics import f1_score, precision_score, recall_score
from tabulate import tabulate

from numpredict import knnestimate
from processData import consume_all
from svmutil import svm_problem, svm_predict, svm_parameter, svm_train
from processData import generate_blogfile, generate_blogfile_stem

# regex to capture the self labeled topic of the blog post
findClass = re.compile("^.+\\((.+)\\)$")

# extract the artist portion. Capture everything until our negative look ahead says we have a space - space "
artistsExtractor = re.compile("^(?!\s\-\s\")([a-zA-Z0-9.&\-']+\s(?:[a-zA-Z0-9.&\-']+\s)*)")

# regex to remove / from my labels for nice file names
rem = re.compile("[^a-z]")

# load the A9 artist to genre file
with open("datafiles/artistsToGenre.json", "r") as agi:
    aTg = json.load(agi)


# read file gotten from clusters.py in A8
def readfile(filename):
    with open(filename, "r") as o:
        lines = [line.rstrip("\n") for line in o]
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        rownames.append(p[0])
        data.append({'input': [float(x) for x in p[1:]], 'result': p[0]})
    return rownames, colnames, data

# using the blogtop500.txt file from A8 do knn on it
def nonstemmeda8():
    # load the data
    blognames, words, data = readfile("datafiles/blogtop500.txt")
    # find out where F-Measure is
    fmeasure_idk = blognames.index('F-Measure')
    # find out where wsdl is
    wsdl_idk = blognames.index('Web Science and Digital Libraries Research Group')
    # remove fmeasure from the data as we do not want to include it
    takeout = data.pop(fmeasure_idk)
    print("http://f-measure.blogspot.com/")
    # hold the results of knn for reporting
    mout = []
    klast = None
    # do knn
    for k in [1, 2, 5, 10, 20]:
        # for reporting I am shortening the output to only include the new data
        # successive knn runs return the same data for previous k values
        # ie k=2 [a,b] then k=5 would be [a,b,c,d,e] I only want k=2[a,b] and k=5[c,d,e]
        if k != 1:
            val = knnestimate(data, data[fmeasure_idk]['input'], k)[klast:]
        else:
            val = knnestimate(data, data[fmeasure_idk]['input'], k)
        klast = k
        mout.append(["%d" % k, ", ".join(val)])
        print("The %d nearest neighbors are:" % k, knnestimate(data, data[fmeasure_idk]['input'], k))
    # write out a table in latex
    headers = ['k', 'nearest neighbors']
    with open("tables/fmeasure-knearest-nonstemmed.text", "w+") as out:
        out.write(tabulate(mout, headers=headers, tablefmt="latex"))
    # do the same for wsdl
    data.insert(fmeasure_idk, takeout)
    print("http://ws-dl.blogspot.com/")
    data.pop(wsdl_idk)
    mout.clear()
    for k in [1, 2, 5, 10, 20]:
        if k != 1:
            val = knnestimate(data, data[fmeasure_idk]['input'], k)[klast:]
        else:
            val = knnestimate(data, data[fmeasure_idk]['input'], k)
        klast = k
        mout.append(["%d" % k, ", ".join(val)])
        print("The %d nearest neighbors are:" % k, knnestimate(data, data[fmeasure_idk]['input'], k))
    headers = ['k', 'nearest neighbors']
    with open("tables/wsdl-knearest-nonstemmed.text", "w+") as out:
        out.write(tabulate(mout, headers=headers, tablefmt="latex"))


def stemmeda8():
    # behave exactly as its non-stemmed counterpart except using the stemmed file
    blognames, words, data = readfile("datafiles/blogtop500_stemmed.txt")
    fmeasure_idk = blognames.index('F-Measure')
    wsdl_idk = blognames.index('Web Science and Digital Libraries Research Group')
    takeout = data.pop(fmeasure_idk)
    mout = []
    klast = None
    print("http://f-measure.blogspot.com/")
    for k in [1, 2, 5, 10, 20]:
        if k != 1:
            val = knnestimate(data, data[fmeasure_idk]['input'], k)[klast:]
        else:
            val = knnestimate(data, data[fmeasure_idk]['input'], k)
        klast = k
        mout.append(["%d"%k, ", ".join(val)])
        print("The %d nearest neighbors are:" % k, knnestimate(data, data[fmeasure_idk]['input'], k))
    headers = ['k', 'nearest neighbors']
    with open("tables/fmeasure-knearest-stemmed.text", "w+") as out:
        out.write(tabulate(mout, headers=headers, tablefmt="latex"))
    data.insert(fmeasure_idk, takeout)
    print("http://ws-dl.blogspot.com/")
    data.pop(wsdl_idk)
    mout.clear()
    for k in [1, 2, 5, 10, 20]:
        if k != 1:
            val = knnestimate(data, data[fmeasure_idk]['input'], k)[klast:]
        else:
            val = knnestimate(data, data[fmeasure_idk]['input'], k)
        klast = k
        mout.append(["%d" % k, ", ".join(val)])
        print("The %d nearest neighbors are:" % k, knnestimate(data, data[fmeasure_idk]['input'], k))
    with open("tables/wsdl-knearest-stemmed.text", "w+") as out:
        out.write(tabulate(mout, headers=headers, tablefmt="latex"))


# execute question 1
def a8():
    nonstemmeda8()
    print("---------------------------------")
    stemmeda8()


# helper method for classification using SVM
# extracts the label for blog structure classification
def blog_structure_helper(name):
    cn = findClass.match(name).group(1).lower().strip()
    if "concert" in cn or 'spotlight' in cn:
        cn = 'concert/spotlight'
    return cn


# helper method for classification using SVM
# extracts the label for genre classification
def blog_genre_helper(name):
    m = artistsExtractor.match(name)
    if m is not None:
        cn = aTg[m.group(1).rstrip(" -")]
    else:
        cn = "R&B/Jazz/Mowtown/Country/Other"
    return cn


# method to execute the 10 fold SVM classification
def tfold_blog(fname, labels, lextractor, outname):
    """
    :param fname: the data file to read in
    :param labels: the labels to be used for classification
    :param lextractor: the label extractor
    :param outname:  the output file name
    """
    # read in the data
    blognames, words, data = readfile(fname)

    # create lookup table for the blog names
    blognameidk = {}
    for i in range(len(blognames)):
        blognameidk[blognames[i]] = i
    # reporting data list
    mout = []
    mout2 = []

    # do 10 fold validation per label
    # each label is expanded to label or not label
    for clazz in labels:
        print(clazz)
        # get a fold instance
        kf = KFold(len(data), 10)
        # holds the results per fold
        kfhMetrics = defaultdict(list)
        ac = []
        tcIndex = 1
        # loop through each folds train and text index
        for train_index, test_index in kf:
            # holders for data results
            train = []
            test = []
            lab = []
            tlab = []
            actualLabels = []
            # make training data
            for i in train_index:
                clazz1 = lextractor(blognames[i])
                if clazz in clazz1:
                    tlab.append(1)
                else:
                    tlab.append(-1)
                train.append(data[i]['input'])
            # make test data
            for i in test_index:
                clazz1 = lextractor(blognames[i])
                test.append(data[i]['input'])
                if clazz in clazz1:
                    lab.append(1)
                    actualLabels.append(clazz)
                else:
                    lab.append(-1)
                    actualLabels.append("not " + clazz)
            # create a problem
            # libsvm 3.21 changed the interface from the example from Toby Segaran
            prob = svm_problem(tlab, train)
            # create parameters: -s 2[one-class svm], -t 0 linear kernel
            param = svm_parameter('-s 2 -t 0')
            # train a model
            m = svm_train(prob, param)
            # get the predicted labels, prediction accuracy
            p_label, p_acc, p_val = svm_predict(lab, test, m=m)
            ac.append(p_acc[0])
            print( p_acc)
            # transform the labels into reportable format
            predictedLabels = [clazz if l == 1.0 else "not " + clazz for l in p_label]
            # take mean of the values as the scikit learn scores returns the values for each label
            kfhMetrics['precision'].append(
                statistics.mean(precision_score(actualLabels, predictedLabels, average=None)))
            kfhMetrics['recall'].append(statistics.mean(recall_score(actualLabels, predictedLabels, average=None)))
            kfhMetrics['f1'].append(statistics.mean(f1_score(actualLabels, predictedLabels, average=None)))
            ac.append(p_acc[0])
            tcIndex += 1
        # create a entry for our report tabel
        ret1 = [clazz, statistics.mean(kfhMetrics['precision']), statistics.mean(kfhMetrics['recall']),
                statistics.mean(kfhMetrics['f1'])]
        mout.append(ret1)
        acc = "%.2f" % statistics.mean(ac)
        mout2.append([ "%s, not %s" % (clazz, clazz), acc + "%"])


    # write out report
    headers = ["label", "precision", 'recall', 'f1']
    with open(outname, "w+") as out:
        out.write(tabulate(mout, headers=headers, tablefmt="latex"))
    headers = [ "label", 'mean accuracy']
    with open(outname+"acc", "w+") as out:
        out.write(tabulate(mout2, headers=headers, tablefmt="latex"))


def do_ten_fold():
    # do ten fold SVM, repeating process done in A9
    bf_nonstemmed = "datafiles/fmeasure.txt"
    bf_stemmed = "datafiles/fmeasure_stemmed.txt"
    blog_structure_labels = ['the song remains the same', 'concert/spotlight', 'lp review', 'forgotten song']
    blog_genre_labels = ['Rock', 'R&B/Jazz/Mowtown/Country/Other', 'Pop/Electronic/Hip-Hop', 'Metal/Punk/Hardcore',
                         'Indie Rock/Alternative']

    tfold_blog(bf_nonstemmed, blog_structure_labels, blog_structure_helper, "tables/tenfold-metrics-structure.txt")
    tfold_blog(bf_stemmed, blog_structure_labels, blog_structure_helper, "tables/tenfold-metrics-structure-stemmed.txt")

    tfold_blog(bf_nonstemmed, blog_genre_labels, blog_genre_helper, "tables/tenfold-metrics-genre.txt")
    tfold_blog(bf_stemmed, blog_genre_labels, blog_genre_helper, "tables/tenfold-metrics-genre-stemmed.txt")


if __name__ == '__main__':
    # read in data-file
    consume_all("datafiles/f-measure.xml")
    generate_blogfile()
    generate_blogfile_stem()
    nonstemmeda8()
    stemmeda8()
    do_ten_fold()
