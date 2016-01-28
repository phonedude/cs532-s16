# RACHEL MCCREARY
# CS 432 ASSIGNMENT 1

from bs4 import BeautifulSoup
import urllib2
import urlparse
import sys

if __name__ == "__main__":

	for arg in sys.argv[1:]:
		uri = arg

	#uri = "http://www.cs.odu.edu/~mln/teaching/cs532-s16/test/pdfs.html"
	#uri = "http://www.ibiblio.org/ebooks/Poe/"
	#uri = "http://www.accesstoinsight.org/lib/list-pdf.html"
	
	page = urllib2.urlopen(uri)
	soup = BeautifulSoup(page.read(), 'html.parser')

	for link in soup.find_all('a'):
		href = link.get('href')
		if href != None:
			if href.startswith("http") == False:
				href = urlparse.urljoin(uri, href)
			response = urllib2.urlopen(href)
			status_code = response.info().getheader('Status')
			content_type = response.info().getheader('Content-Type')

			if content_type == "application/pdf":
				print href
				size_of_pdf = response.info().getheader('Content-Length')
				print size_of_pdf, " bytes"
