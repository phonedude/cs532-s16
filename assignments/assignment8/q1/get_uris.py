#! /usr/bin/env python

import requests
import sys
from bs4 import BeautifulSoup

default = 'http://www.blogger.com/next-blog?navBar=true&blogID=3471633091411211117'
must_haves = ['http://f-measure.blogspot.com/', 'http://ws-dl.blogspot.com/']

def get_atom(uri):
	try:
		r = requests.get(uri)
	except Exception, e:
		return None
	soup = BeautifulSoup(r.text)
	links = soup.find_all('link', {'type':'application/atom+xml'})
	if links: 
		return str(links[0]['href'])
	return None

def add_uri(uri, uris, outfile):
	if uri and uri not in uris:
		uris.add(uri)
		outfile.write(uri + '\n')
		print len(uris), uri

if __name__ == '__main__':
	uris = set()
	with open('blog_uris', 'a') as outfile:
		if len(sys.argv) > 1 and sys.argv[1] == 'new':
			for must_have in must_haves:
				uri = get_atom(must_have)
				add_uri(uri, uris, outfile)
		else:
			with open('blog_uris') as infile:
				[uris.add(line.strip()) for line in infile]
		while len(uris) < 100:
			uri = get_atom(default)
			add_uri(uri, uris, outfile)