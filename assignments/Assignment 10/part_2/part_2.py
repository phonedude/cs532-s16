# coding=utf-8
import docclass
import feedfilter
import feedparser
import sys
import urllib2
from docclass import fisherclassifier
from urllib2 import urlopen
from bs4 import BeautifulSoup
import clusters
import numpredict

reload(sys)
sys.setdefaultencoding('utf-8')

#cl = docclass.fisherclassifier(docclass.getwords)
#cl.setdb('rachel.db')
#feedfilter.read('full_rss.txt', cl)

# making a fake RSS with 100 entries instead of just 10

reload(sys)
sys.setdefaultencoding('utf-8')

with open('teaser_links.txt') as f:
  for line in f:
    url = line
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    title = soup.find(class_="entry-title").getText()
    summary = soup.find(class_="format_text entry-content").getText()

    # Changing this to print new file per blog entry, to make generating feed vector easier

    try:
        new_file = open(title+'.txt', 'w')
        print >> new_file, '<?xml version="1.0" encoding="UTF-8" ?>'
        print >> new_file, 'rss version ="2.0">'
        print >> new_file, '<channel>'
        print >> new_file, '<title>' + title + '</title>'
        print >> new_file, '<item>'
        print >> new_file, '<title>' + title + '</title>'
        print >> new_file, '<description>' + summary + '</description>'
        print >> new_file, '</item>'
        print >> new_file, '</channel>'
        print >> new_file, '</rss>'
        new_file.close()

      except:
        pass


