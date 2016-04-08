import sys
import os
import os.path
import feedparser
import urllib2
import time
import chardet
from bs4 import BeautifulSoup

outputFile = open("feedNames.txt", 'w')

def dereferenceUri(uri):

    pagehandle = urllib2.urlopen(uri)
    pagedata = pagehandle.read()
    derefurl = pagehandle.geturl()
    pagehandle.close()

    return pagedata,derefurl

def getAtomFeedUri(html):

    soup = BeautifulSoup(html) 

    atomLinks = soup.find_all('link',
        attrs = { 'rel' : 'alternate', 'type' : 'application/atom+xml' })

    # we assume there is only one atom link
    atomURI = atomLinks[0].attrs['href']

    return atomURI

def meetsCriteria(feedText):

    parsedData = feedparser.parse(feedText)

    # assume we're good to go by default (fail optimistic?)
    goodToGo = True

    sys.stderr.write("blog has " + str(len(parsedData.entries)) + " entries\n")

    if (len(parsedData.entries) < 25):
        goodToGo = False        

    #if (chardet.detect(feedText)['encoding'] != 'ascii'):
    #    sys.stderr.write("blog charset is " + chardet.detect(feedText)['encoding'] +
    #        ", likely won't parse well for feed vector\n")
    #    goodToGo = False

    return goodToGo

def getNextUri():

    uri = "http://www.blogger.com/next-blog?navBar=true&blogID=4244952099341869447"

    pagehandle = urllib2.urlopen(uri)
    nexturi = pagehandle.geturl()
    pagehandle.close() 

    return nexturi


if __name__ == "__main__":

    feedlist = []
    feedlist.append("http://f-measure.blogspot.com/feeds/posts/default?max-results=200")
    feedlist.append("http://ws-dl.blogspot.com/feeds/posts/default?max-results=200")

    while (len(feedlist) <= 100):

        try:
            # Tried these steps, but realized I would have to
            # parse JavaScript
            # * look for the iframe containing the next button
            #       <iframe name='navbar-iframe'...
            # iframeURI = getIframeUri(html)
            # * dereference the link from that iframe
            # iframeText = getIframeText(iframeURI)
            # * extract the uri form
            # <a class="b-link" href="...">Next Blog</a>
            # uri = getNextUri(iframeText)
            uri = getNextUri()
        except urllib2.HTTPError as e:
            sys.stderr.write("failed to acquire next uri, delaying 5 seconds\n")
            time.sleep(5)
        else:
            sys.stderr.write("working on URI " + uri + "\n")
    
            try:
                # dereference the uri and get text
                html,derefuri = dereferenceUri(uri)
            except urllib2.HTTPError as e:
                sys.stderr.write("failed to dereference " + uri +
                    ", delaying 5 seconds\n")
                time.sleep(5)
            else:
                try:
                    # fetch the atom feed URI
                    feedURI = getAtomFeedUri(html)
                    sys.stderr.write("acquired feed URI " + feedURI + "\n")
                except IndexError as e:
                    sys.stderr.write(
                        "failed to acquire Atom feed from HTML, delaying 5 seconds\n")
                else:
                    try:
                        # get the atom feed text
                        feedText,feedURI = dereferenceUri(feedURI)
                    except urllib2.HTTPError as e:
                        sys.stderr.write("failed to dereference " + feedURI +
                            ", delaying 5 seconds\n")
                        time.sleep(5)
                    else:
                        # if it meets the criteria, save the file
                        if meetsCriteria(feedText):
                            sys.stderr.write("Saving blog feed " + feedURI + "?max-results=1000\n")
                            feedlist.append(feedURI + "?max-results=1000")
        
                        # be nice to the site
                        time.sleep(1)

    for feed in feedlist:
        print feed
        outputFile.write(str(feed))
        outputFile.write("\n")

outputFile.close()