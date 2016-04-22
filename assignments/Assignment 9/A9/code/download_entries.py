import urllib2
from urllib2 import urlopen
from bs4 import BeautifulSoup

url = "http://www.chefeddy.com/page/"
page_number = 1
for page_number in range(1, 11):
	new_url = url + str(page_number) + '/'
	page = urllib2.urlopen(new_url)
	soup = BeautifulSoup(page, "html.parser")
	teaser_links = soup.find_all(class_='teaser_link')
	# print (str(teaser_link).replace('\u2192', ''))
	for s in teaser_links:
		print (s['href'])
	page_number = page_number + 1
