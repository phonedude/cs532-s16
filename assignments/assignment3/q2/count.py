#! /usr/bin/python

import os
import re
import sys
import pickle
import math
from string import punctuation

map_file = open('uri_map', 'rb')
uri_map = pickle.load(map_file)

def count_terms(term, file_list=os.listdir('html/processed')):
	for filename in file_list:
		with open('html/processed/' + filename + '.processed.txt') as infile:
			uri = infile.readline().strip()
			text = infile.read()
			count = text.count(term)
			if count > 0:
				print('{} {}'.format(count, uri))
				return count, uri
	return None, None

def get_uri(uri):
	for filename in os.listdir('html/processed/'):
		with open('html/processed/' + filename + '.processed.txt') as infile:
			if uri in infile.readline():
				return uri, filename
	return None, None

def get_uris():
	uri_file = {}
	for uri in open('links').read().split('\n'):
		uri, filename = get_uri(uri)
		if not uri:
			continue
		uri_file[uri] = filename
	return uri_file

def get_filename(uri):
	if uri_map.has_key(uri):
		return uri_map[uri]
	return None

def strip_html(filename):
	if not filename:
		print 'invalid filename'
		return
	with open('html/processed/' + filename + '.processed.txt') as infile:
		# To remove URI in first line
		infile.readline()
		# Removing all punctuation
		strs = infile.read()
		r = re.compile(r'[{}]'.format(punctuation))
		content = r.sub(' ', strs)
		return content

def get_tf(content, term):
	return float(content.count(term)) / float(len(content.split()))

def get_idf(term):
	present = set()
	absent = set()
	for uri, filename in uri_map.iteritems():
		content = strip_html(filename)
		if not content:
			continue
		if term in content:
			present.add(uri)
		else:
			absent.add(uri)
	return math.log(float(len(absent)) / float(len(present)), 2)

def process_uri(uri, term):
	tf = get_tf(strip_html(get_filename(uri)), term)
	tfidf = tf * idf
	return tf, tfidf

idf = get_idf('allu arjun')

if __name__ == '__main__':
	# Used to bulk print all occurences > 0 of search term
	if len(sys.argv) == 3 and sys.argv[1] == 'count':
		count_terms(sys.argv[2], os.listdir('html/processed'))

	# Used to build the uri_map file, which maps the uri to 
	# the filename the dereferenced content is stored in
	elif len(sys.argv) == 2 and sys.argv[1] == 'uri_map':
		uris = get_uris()
		pickle.dump(uris, open('uri_map', 'w'))

	# Used to count occurences of the search term in a list
	# of URIs specified in the 'uri_counts' file
	elif len(sys.argv) == 4 and sys.argv[1] == 'count':
		with open('uri_counts', 'w') as outfile:
			for uri, filename in uri_map.iteritems():
				count, uri = count_terms(sys.argv[2], [filename])
				outfile.write('{} {}\n'.format(count, uri))

	# Used as a utility to simply get the filename for the given URI
	elif len(sys.argv) == 3 and sys.argv[1] == 'uri':
		print get_filename(sys.argv[2])

	# Used to calculate all tf, idf, tfidf values and write them to a file
	# for a selection of URIs
	elif len(sys.argv) == 3 and sys.argv[1] == 'calc':
		term = sys.argv[2]
		with open('uri_counts') as infile:
			uris = uris = [line.split()[1] for line in infile.read().split('\n')]
			with open('uri_frequencies', 'w') as outfile:
				outfile.write('{:<7} {:<7} {:<7} {:<7}\n'.format('TFIDF', 'TF', 'IDF', 'URI'))
				for uri in uris:
					tf, tfidf = process_uri(uri, term)
					outfile.write('{:5.4f}  {:5.4f}  {:5.4f}  {}\n'.format(tfidf, tf, idf, uri))
	else:
		print('Usage:\n\tpython grep.py <SEARCH_TERM>')