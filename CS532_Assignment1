#Author- Gabriel Marquez, Matthew Payne, Catherine Nguyen
#Date- 01/28/2016
#Name CS532_Assignment1
#Additional instuction
#Import libraries
from bs4 import BeautifulSoup
import urllib2
import requests
import ssl
#Get website url file url
url = raw_input("Enter URL: ")

File = urllib2.urlopen(url)
Html = File.read()
File.close()
soup = BeautifulSoup(Html, "html.parser")

for links in soup.find_all('a'):
    a = links.get('href')
    c = 'http'
    d = a[0:3]
    if c == d:
        pass
    b = requests.head(a)
    c = 'http'
    d = a[0:3]
    if c == d:
        pass
    
    #goes through the list of links on the page and checks status
    elif  b.status_code >= 300 and b.status_code < 400:
        while b.status_code != 200:
            redi = urllib2.build_opener(urllib2.HTTPRedirectHandler)
            request = redi.open(a)
            a = request.url
            b = requests.head(a)
            
        #checks the url to see if it ends in .pdf    
        a1 = '.pdf'
        b1 = a[-4:]
        if a1 == b1:
            print (a)
            pdf = urllib2.urlopen(a)
            bytez = pdf.headers["Content-Length"]
            print bytez + ' bytes'
    
    #if it ends in .pdf, it will print out the url and the amount of bytes it contains
    elif b.status_code == 200:
        a1 = '.pdf'
        b1 = a[-4:]
        if a1 == b1:
            print (a)
            pdf = urllib2.urlopen(a)
            bytez = pdf.headers["Content-Length"]
            print bytez + ' bytes'
        
    else:
        pass
