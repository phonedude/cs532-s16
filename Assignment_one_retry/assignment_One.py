# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import urllib2
import certifi
import sys

def getFileAndInformation(url):
    urlFile = urllib2.urlopen(url)
    data = urlFile.read()
    print urlFile.getcode()
    print urlFile.info()
    urlFile.close()
    return data

def getInformation(url):     #Gets the main information from the url's that are looped through.
    urlFile = urllib2.urlopen(url)
    data = urlFile.read()
    if urlFile.info().getheader('Content-Type') == "application/pdf": #Only shows information if the type is pdf
        print url
        print "Content Type: "
        print urlFile.info().getheader('Content-Type')
        print "Number of bytes in file: "
        print urlFile.info().getheader('Content-Length')
        print "Response code: "		
        print urlFile.getcode()
        print"***********************PDF FILE******************************"
    urlFile.close()
    

print"*************************************************************"
print "This is the name of the script: ", sys.argv[0] #Grabs the script name
print"*************************************************************"
print "This is the name of the URI to check: ", sys.argv[1]  #Grabs the argument name


urlMain = sys.argv[1]

data = getFileAndInformation(urlMain)

print"*************************************************************"
print"Now I am going to post all of the linked pdf files!"
print"***********************PDF FILE******************************"

soup = BeautifulSoup(data, "html.parser")   #Loops through all of the links in the page and sends them to the function to sort
for link in soup.find_all('a'):  
    if getInformation(link.get('href')) is not None:
        print getInformation(link.get('href'))
	
