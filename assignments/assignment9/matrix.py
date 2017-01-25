import feedparser
import futures
import math
import md5
import re
import sys
import json

blog_uri = 'http://kevinmorrow.blogspot.com/feeds/posts/default'
data_file = 'blog_content'

def get_next(d):
	for item in d.feed.links:
		if item['rel'] == u'next':
			return item['href']
	return None

def parse_entries(entries, uri):
	print('processing {}'.format(uri))
	next = uri
	while next is not None:
		feed = feedparser.parse(next)
		next = get_next(feed)
		print('next {}'.format(next))
		for entry in feed.entries:
			if entry.title in entries:
				continue
			entries.append(entry.title)
			if len(entries) >= 100:
				next = None
				break
	return entries

def load_data(filename):
	entries = []
	with open(filename) as infile:
		return [entry.strip() for entry in infile]

if __name__ == '__main__':
	old_entries = load_data(data_file)
	entries = parse_entries(old_entries, blog_uri)
	with open(data_file, 'w') as outfile:
		for entry in entries:
			outfile.write(entry + '\n')
