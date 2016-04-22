# coding=utf-8
import docclass
import feedfilter
import feedparser
import sys
import urllib2
from docclass import fisherclassifier
from urllib2 import urlopen
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
cl = docclass.fisherclassifier(docclass.getwords)

#cl.setdb('test.db')
#feedfilter.read('test_rss_manual.txt', cl)
#feedfilter.read('test_rss_cl.txt', cl)

cl.setdb('rachel.db')
#feedfilter.read('manual_classify_rss.txt', cl)
#feedfilter.read('cl_classify_rss.txt', cl)

#print 'Number of entries about chocolates: ' + str(cl.catcount('chocolates'))
#print 'Categories: ' + str(cl.categories())
#print 'Coffee Caramels | category: ' + str(cl.classify('Coffee Caramels'))
#print cl.fisherprob('tempered', 'chocolates')

# making a fake RSS with 100 entries instead of just 10
"""
reload(sys)
sys.setdefaultencoding('utf-8')
print '<?xml version="1.0" encoding="UTF-8" ?>'
print 'rss version ="2.0">'
print '<channel>'
with open('teaser_links.txt') as f:
  for line in f:
    url = line
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    title = soup.find(class_="entry-title").getText()
    summary = soup.find(class_="format_text entry-content").getText()
    print '<item>'
    print '<title>' + title + '</title>'
    print '<description>' + summary + '</description>'
    print '</item>'
print '</channel>'
print '</rss>'
"""