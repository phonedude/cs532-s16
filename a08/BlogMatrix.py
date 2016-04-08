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

from lib.WEBlib import AddURI
from TwitterSearch import *

__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  Apr 05, 2016 at 11:54:30'
__email__ = 'pvargas@cs.odu.edu'

"""
Grabs 100 blogs; including:

http://f-measure.blogspot.com/
http://ws-dl.blogspot.com/

"""
root_url_array = []
all_links_set = set()
final_link = ''


def main():
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    urilist = set()
    apcount = {}
    wordcounts = {}
    feedlist = []

    urilist.add('http://f-measure.blogspot.com/')
    urilist.add('http://ws-dl.blogspot.com/')

    for uri in urilist:
        title, wc = getallpages(uri)
        if title:
            wordcounts[title] = wc
            print(title, wordcounts[title])
            for word, count in wc.items():
                apcount.setdefault(word, 0)
                if count > 1:
                    apcount[word] += 1
            feedlist.append(uri)
            urilist.add(uri)

    while len(urilist) < 100:
        lasturi = set()
        AddURI(lasturi, 'http://www.blogger.com/next-blog?navBar=true&blogID=3471633091411211117')

        print('Getting word count....')
        for uri in lasturi:
            uri = re.match('(^.*\.com\/)(?!expref)', uri).group(0)
            if uri not in urilist:
                title, wc = getallpages(uri)
                if title:
                    wordcounts[title] = wc
                    print(len(urilist), title, wordcounts[title])
                    for word, count in wc.items():
                        apcount.setdefault(word, 0)
                        if count > 1:
                            apcount[word] += 1
                    feedlist.append(uri)
                    urilist.add(uri)

                else:
                    print('Discarding URI...')

    wordlist = []
    for w, bc in apcount.items():
        frac = float(bc) / len(feedlist)
        if 0.5 > frac > 0.1:  wordlist.append(w)

    out = open('blogdata.txt', 'w')
    out.write('Blog')
    for word in wordlist[:500]: out.write('\t%s' % word)
    out.write('\n')
    for blog, wc in wordcounts.items():
        print(blog)
        out.write(blog)
        for word in wordlist[:500]:
            if word in wc: out.write('\t%d' % wc[word])
            else: out.write('\t0')
        out.write('\n')
    out.close()

    out = open('feedlist.txt', 'w')
    for uri in urilist:
        out.write('%s\n' % uri)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))

    return


def getallpages(uri):
    twc = None
    rss_feed = uri + 'feeds/posts/default/'
    title, wc = getwordcounts(rss_feed)
    if title:
        print('Getting linkpages....', title)
        twc = linkpages(wc, rss_feed)

    if not twc:
        return '', ''

    return title, twc


def linkpages(wc, rss_feed):
    twc = {}
    for word, count in wc.items():
        twc.setdefault(word, 0)
        twc[word] += count

    flag = True
    while flag:
        page = requests.get(rss_feed).text
        soup = BeautifulSoup(page, 'html.parser')
        for link in soup.find_all('link'):
            t = link.get('rel')
            if t and t[0] == 'next':
                print('Getting %s ...' % link.get('href'))
                title, wc = getwordcounts(link.get('href'))

                rss_feed = link.get('href')
                for word, count in wc.items():
                    twc.setdefault(word, 0)
                    twc[word] += count

                print(twc)
                break

        if t and t[0] != 'next':
            flag = False
        if not t:
            flag = False

    return twc


def getwordcounts(rss_feed):
    # Parse the feed
    d = feedparser.parse(rss_feed)
    wc = {}

    # Loop over all the entries
    for e in d.entries:
        if 'summary' in e: summary = e.summary
        else: summary = e.description

        # Extract a list of words
        words = getwords(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    if 'title' not in d['feed']:
        d['feed']['tittle'] = ''
        d.feed.title = ''

    return d.feed.title, wc


def getwords(html):
    # Remove all the HTML tags
    txt=re.compile(r'<[^>]+>').sub('', html)

    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # Convert to lowercase
    return [word.lower() for word in words if word != '']


if __name__ == '__main__':
    main()
    sys.exit(0)