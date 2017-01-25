# -*- encoding: utf-8 -*-
#! /usr/bin/python

import requests
import re

MW_URI = "http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/"

if __name__ == '__main__':
	with open('output', 'r') as f:
		output = open('site_mementos', 'w')
		mementos = {}
		for uri in f.read().split('\n'):
			if uri is '':
				continue
			count = 0
			target_uri = MW_URI + uri
			while True:
				result = requests.get(target_uri)
				if result.ok:
					count = count + result.text.count('rel="memento"')
				last_line = result.text.split('\n')[-1]
				if 'rel="timemap"' not in last_line:
					break
				sites = re.findall(r'<([^<|^>]+)>', last_line)
				target_uri = sites[1]
			mementos[uri] = count
			print 'found %d mementos for uri: %s' % (count, uri)
			output.write('%s %d\n' % (uri, count))
	output.close()