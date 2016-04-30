import re
import sys
import os
import feedparser
import functools
from time import strftime, localtime, time

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import a9.docclass as t

__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  Apr 19, 2016 at 12:50:26'
__email__ = 'pvargas@cs.odu.edu'

"""
Grabs 100 blog entries from http://www.insidehoops.com/blog/:

http://f-measure.blogspot.com/
http://ws-dl.blogspot.com/

"""
root_url_array = []
final_link = ''
wordcounts = {}
all_titles = []

def main():
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    apcount = {}
    total_entries = 0


    #url_blog = (lambda x: 'http://www.insidehoops.com/blog/?feed=rss2&paged=%s' % x)
    #output = (lambda x: 'www-insidehoops-com-blog-feed-rss2-paged-%s' % x)
    indata = (lambda x: 'www-insidehoops-com-blog-feed-rss2-paged-%s' % x)
    x = 0

    # generating 100 entries from blog
    print('Generating 100 blog entries ...')
    while total_entries < 100:
        x += 1
        title, wc, entries = getwordcounts(indata(x))

        """
        # write raw data
        print('Writing raw data ....')
        file = open(output(x), 'w')
        page = requests.get(url_blog(x)).text
        file.write(page)
        file.close()
        """

        total_entries += entries

        for word, count in wc.items():
            apcount.setdefault(word, 0)
            apcount[word] += count


    # make term discrimination
    print('Filtering terms ...')
    wordlist = []
    for w, bc in apcount.items():
        frac = float(bc) / total_entries
        if 0.7 > frac > 0.0:  wordlist.append(w)

    for title in wordcounts:
        entry_words = set(wordcounts[title])
        for word in set(wordcounts[title]):
            if word not in wordlist:
                print('Deleting %s from item %s...' % (word, title), title)
                entry_words.remove(word)
        wordcounts[title] = list(entry_words)

    # print(total_entries, url_blog(x))
    print(apcount)
    print(wordlist)


    # write entry description into training table
    print('Adding entries into training table ....')
    c1 = t.fisherclassifier(t.getwords)

    x = 0
    for title in all_titles:
        x += 1
        print(x, " ".join(wordcounts[title]))
    c1.add_training_data(wordcounts, all_titles)

    # set the actual categories for entries
    print('Updating actual categories ...')
    c1.set_categories('categories.txt')

    # train the first 50 entries of 100 blog entries
    print('Training first 50 entries from the blog ....')

    for id, text, category in c1.get_data('select trn_id, words, cat_id from training_tb order by trn_id;'):
        if id < 51:
            print(id, text, category)
            c1.train(text, category)

    # determine best class
    tp = {}
    fp = {}
    cat_description = []

    # get all categories
    cat_list = c1.get_data('select cat_id, description from category_tb order by cat_id;')
    for cat in cat_list:
        cat_description.append(cat[1])
        cat = cat[0]
        tp[cat] = 0
        fp[cat] = 0

    print('Determining best class using Fisher classifier ....')
    true_category = []
    for category in c1.get_data('select cat_id from training_tb order by trn_id;'):
        true_category.append(category[0])

    outfile = open('fisher-result.txt', 'w')
    outfile.write('\\begin{table}[!htbp]\n')
    outfile.write('\\caption{Fisher-Result} \label{tab:fisher-result}\n')
    outfile.write('\\begin{center}\n')
    outfile.write('\\vspace{-5mm}\n')
    outfile.write('\\begin{tabular}{ l l l l}\n')
    outfile.write('\\hline\n')
    outfile.write('Title & Predicted Category & Actual Category & Fisherprob()\\\\\ \n')
    outfile.write('\\hline\n')

    # initialize confusion matrix
    c_matrix = [[0 for i in range(8)] for j in range(8)]
    k = 0
    for title in all_titles:
        k += 1
        fisher_cat = c1.classify(" ".join(wordcounts[title]))
        c1.update_fisher_cat(k, fisher_cat)
        print(k, title, true_category[k - 1], fisher_cat)
        if fisher_cat == true_category[k - 1]:
            c_matrix[fisher_cat - 1][fisher_cat - 1] += 1
            tp[fisher_cat] += 1
        else:
            fp[fisher_cat] += 1
            c_matrix[true_category[k - 1] - 1][fisher_cat - 1] += 1

        fisher_prob = c1.fisherprob(" ".join(wordcounts[title]), true_category[k - 1])
        outfile.write('%s & %s & %s & %.4f\\\\\n' % (title, cat_description[fisher_cat - 1],
                                                 cat_description[true_category[k - 1] - 1],
                                                 fisher_prob))
    outfile.close()

    print('\n\nCat\t TP \t FP \t Precision \t TGC \t Recall \t F-measure')
    for cat in cat_list:
        cat = cat[0]
        total_g_matrix = functools.reduce(lambda x, y: x + y, c_matrix[cat - 1])
        precision = tp[cat] / (tp[cat] + fp[cat])
        recall = tp[cat] / total_g_matrix
        print('%d \t %d \t %d %.4f \t %d \t %.4f \t %.4f' % (cat, tp[cat], fp[cat],
                                                             precision,
                                                             total_g_matrix, recall,
                                                             2 * precision * recall / (precision + recall)))


    print(c_matrix)
    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))

    return


def getwordcounts(rss_feed):
    # from a file
    f = open(rss_feed, 'r')
    data = f.read()
    f.close()

    # Parse the feed
    #d = feedparser.parse(rss_feed)
    d = feedparser.parse(data)
    wc = {}

    entries = 0
    # Loop over all the entries
    for e in d.entries:
        entries += 1
        if 'summary' in e: summary = e.summary
        else: summary = e.description

        # Extract a list of words
        words = getwords(e.title + ' ' + summary)
        print(entries, e.title, getwords(summary))
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

        wordcounts[e.title] = [y for y in words]
        all_titles.append(e.title)


    if 'title' not in d['feed']:
        d['feed']['tittle'] = ''
        d.feed.title = ''

    return d.feed.title, wc, entries


def getwords(html):
    # Remove all the HTML tags
    txt=re.compile(r'<[^>]+>').sub('', html)

    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # Convert to lowercase
    return [word.lower() for word in words if word != '' and len(word) > 2]


if __name__ == '__main__':
    main()
    sys.exit(0)