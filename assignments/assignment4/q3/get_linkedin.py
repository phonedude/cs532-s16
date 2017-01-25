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
import oauth2 as oauth
import time

consumer = oauth.Consumer(
     key="",
     secret="")
token = oauth.Token(
     "", 
     secret=""
     )
client = oauth.Client(consumer, token)

url = "http://api.linkedin.com/v1/people/~/connections:(num-connections,first-name,last-name)"

resp, content = client.request(url)
soup = BeautifulSoup(content)
i = 0
all = 0
print '%-15s %-20s' %('Connections','LinkedIn User Name')	
for message in soup.find_all('person'):
	all += 1
	if len(message.find_all('num-connections')) > 0:
		i += 1
		fullName = message.find('first-name').text+' '+ message.find('last-name').text
		print '%-15s %-20s' %(message.find('num-connections').text, fullName)
		with open('linkedin', 'a') as outfile:
			outfile.write('%-15d %-20s\n' %(init_url['friends_count'],init_url['screen_name'].encode('ascii', 'replace')))
		
print "\nNumber of Naina Sai's LinkedIn connections is "+str(all)+'(can not retrieve data of '+str(all - i)+' connection(s)) '