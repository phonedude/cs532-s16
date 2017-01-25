# -*- encoding: utf-8 -*-
#! /usr/bin/python
from __future__ import unicode_literals
import xml.etree.cElementTree as et
from bs4 import BeautifulSoup
from urlparse import parse_qs
import unicodedata
import urllib2
import re
import os
import sys

print '%-15s %-20s' %('Friends-count','Friend-screen-name')	

file = "mln.graphml"
handler = open(file).read()
soup = BeautifulSoup(handler)
i = 0
all = 0
for message in soup.find_all('node'):
	all += 1
	foo = et.XML(str(message))
	name = ''
	for e in foo:
		if ('graphml_count' in str(e.items())):
			print '%-15s %-20s' %(e.text,name)
			with open('friend_counts', 'a') as outfile:
				outfile.write('%-15s %-20s\n' %(e.text,name))
			i += 1
		if ('name' in str(e.items())):
			name = e.text
print "\nNumber of Dr. Nelson's friends ,who allow to retrieve their friends count, is "+str(i)+" out of "+str(all)