import feedparser
import urllib
from urllib.request import urlopen

feed = feedparser.parse('http://www.chefeddy.com/feed/')
for entry in feed['entries']:
	content = urlopen(entry['link']).read()
	print (content)
