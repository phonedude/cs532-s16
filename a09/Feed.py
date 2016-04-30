import re
import sys
import os
import feedparser
import requests
from bs4 import BeautifulSoup
from time import strftime, localtime, time

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import a9.docclass as t

__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  Apr 19, 2016 at 12:50:26'
__email__ = 'pvargas@cs.odu.edu'

"""
Grabs 100 blogs; including:

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
    indata = (lambda x: 'www-insidehoops-com-blog-feed-rss2-paged-%s.old' % x)
    x = 0

    # generating 100 entries from blog
    while total_entries < 100:
        x += 1
        title, wc, entries = getwordcounts(indata(x))

        """
        # write raw data
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
    wordlist = []
    for w, bc in apcount.items():
        frac = float(bc) / total_entries
        if 0.5 > frac > 0.0:  wordlist.append(w)

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

    """
    # write entry description into training table
    c1 = t.naivebayes(t.getwords)
    for x in range(1, total_entries + 1):
        print(x, " ".join(wordcounts[x]))
    c1.add_training_data(wordcounts)
    """

    # determine best class
    c1 = t.fisherclassifier(t.getwords)
    true_category = []
    for category in c1.get_data('select cat_id from training_tb order by trn_id;'):
        true_category.append(category)
    k = 0
    for title in all_titles:
        k += 1
        print(k, title, true_category[k - 1], c1.classify(" ".join(wordcounts[title])))


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