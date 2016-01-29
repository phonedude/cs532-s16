#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from bs4 import BeautifulSoup
import urllib



def getLinks(arg):
	f = open ("output_file.txt", "a")
	url = urllib.urlopen(arg)
	htmlPage = url.read()
	f.write(url.geturl())
	url.close()
	soup = BeautifulSoup(htmlPage)
	for links in soup.find_all('a'):
	    f.write(links.get('href')) 
	f.close
	return
	
#call the function  	
for arg in sys.argv:
    print(arg)
    getLinks(arg)