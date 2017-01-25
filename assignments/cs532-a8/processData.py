from collections import defaultdict
from operator import add

from functional import seq
from nltk.stem.snowball import EnglishStemmer

import clusters


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
    feedData = seq.json("datafiles/blogdata.json").map(lambda fe: feed(fe)).to_list()  # type: list[feed]
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
        .filter(lambda wc: wc[1] > 10) \
        .map(lambda wc: (wc[0], 1)) \
        .reduce_by_key(add) \
        .filter(filter_fun) \
        .order_by(lambda wc: -wc[1]) \
        .take(500) \
        .map(lambda wc: wc[0]) \
        .to_list()
    # sort alphabetically
    top500 = sorted(top500)
    print(len(top500))
    # write resultant to file
    with open("datafiles/blogtop500.txt", "w+") as out:
        out.write("Blog\t%s\n" % '\t'.join(top500))
        for tf in sorted(feedData, key=lambda f: f.title):
            out.write(output(tf, top500))


def generate_blogfile_stem():
    # same as non-stem except use stemmed data
    feedData = seq.json("datafiles/blogdata.json").map(lambda fe: feed(fe, True)).to_list()  # type: list[feed]
    top500 = seq(feedData).flat_map(lambda f: list(f.stemCount.items())) \
        .filter(lambda wc: wc[1] > 1) \
        .map(lambda wc: (wc[0],1))\
        .reduce_by_key(add) \
        .filter(filter_fun) \
        .order_by(lambda wc: -wc[1]) \
        .take(500) \
        .map(lambda wc: wc[0]) \
        .to_list()
    top500 = sorted(top500)
    print(len(top500))
    with open("datafiles/blogtop500_stemmed.txt", "w+") as out:
        out.write("Blog\t%s\n" % '\t'.join(top500))
        for tf in sorted(feedData, key=lambda f: f.title):
            out.write(output_stem(tf, top500))


def do_non_stem():
    # generate the blog file
    generate_blogfile()
    # read the data in
    blognames, words, data = clusters.readfile('datafiles/blogtop500.txt')
    # do clustering
    clust = clusters.hcluster(data)
    # write out asci denogram
    with open("datafiles/blogtop500_asciideno.txt", "w+") as out:
        clusters.printclust2file(clust, out, labels=blognames)
    # generate jpg version of same denogram
    clusters.drawdendrogram(clust, blognames, jpeg='datafiles/blogtop500_deno.jpg')
    # do kmeans and log to file
    with open("datafiles/kmeans_blogtop500.txt", "w+") as kout:
        for k in [5, 10, 20]:
            print("For k=%d" % k)
            kout.write("K=%d\n" % k)
            kout.write("Iterations\n")
            # kmeans for value k
            centriods = clusters.kcluster_toFile(data, k=k, out=kout)
            kout.write("Centroid Values\n-------------------------\n")
            # log centroid values
            for count, centriod in enumerate(centriods, 1):
                print("Centroid #%d" % count)
                kout.write("Centroid #%d\n" % count)
                values = []
                for idx in centriod:
                    print(blognames[idx])
                    values.append(blognames[idx])
                kout.write("%s\n" % ', '.join(values))
            kout.write("=================================\n")
            print("-------")
    # do the dimensionality reduction
    with open("datafiles/dimensionReductionNonStemmed.txt","w+") as dout:
        scaled = clusters.scaledown_logiter(data,out=dout)
    # generated the similar blog jpg
    clusters.draw2d(scaled, blognames, jpg='datafiles/blogtop500_clust2d.jpg')


def do_stemmed():
    generate_blogfile_stem()
    blognames, words, data = clusters.readfile('datafiles/blogtop500_stemmed.txt')
    clust = clusters.hcluster(data)
    with open("datafiles/blogtop500stemmed_asciideno.txt", "w+") as out:
        clusters.printclust2file(clust, out, labels=blognames)
    clusters.drawdendrogram(clust, blognames, jpeg='datafiles/blogtop500stemmed_deno.jpg')

    with open("datafiles/kmeans_blogtop500stemmed.txt", "w+") as kout:
        for k in [5, 10, 20]:
            print("For k=%d" % k)
            kout.write("K=%d\n" % k)
            kout.write("Iterations\n")
            centriods = clusters.kcluster_toFile(data, k=k, out=kout)
            kout.write("Centroid Values\n-------------------------\n")
            for count, centriod in enumerate(centriods, 1):
                print("Centroid #%d" % count)
                kout.write("Centroid #%d\n" % count)
                values = []
                for idx in centriod:
                    print(blognames[idx])
                    values.append(blognames[idx])
                kout.write("%s\n" % ', '.join(values))
            kout.write("=================================\n")
            print("-------")
    with open("datafiles/dimensionReductionStemmed.txt", "w+") as dout:
        scaled = clusters.scaledown_logiter(data, out=dout)
    clusters.draw2d(scaled, blognames, jpg='datafiles/blogtop500stemmed_clust2d.jpg')


if __name__ == "__main__":
    do_non_stem()
    do_stemmed()




