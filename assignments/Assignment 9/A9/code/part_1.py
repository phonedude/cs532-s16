import urllib2
from urllib2 import urlopen
from bs4 import BeautifulSoup
import sys

if __name__ == '__main__':

  reload(sys)
  sys.setdefaultencoding('utf-8')
  with open('teaser_links.txt') as f:
    for line in f:
      url = line
      page = urllib2.urlopen(url)
      soup = BeautifulSoup(page, "html.parser")
      title = soup.find(class_="entry-title").getText()
      entry = soup.find(class_="format_text entry-content").getText()

      try:
        new_file = open(title+'.txt', 'w')
        print >> new_file, entry
        new_file.close()

      except:
        pass

#      print (docclass.getwords(entry))