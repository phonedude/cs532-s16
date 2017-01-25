from __future__ import unicode_literals, print_function
import ttp
import requests
import urllib2

def follow_shortlinks(shortlinks):
	links_followed = {}
	for shortlink in shortlinks:
		url = shortlink
		request_result = requests.get(url)
		redirect_history = request_result.history
		all_urls = []
		for redirect in redirect_history:
			all_urls.append(redirect.url)
		all_urls.append(request_result.url)
		links_followed[shortlink] = all_urls
	return links_followed

def on_error(self, status):
	pass

if __name__ == '__main__':

	shortlinks = []

	with open('short_links.txt')as f:
		for line in f:
			shortlinks.append(line)

	followed_shortlinks = (follow_shortlinks(shortlinks))

	for link in followed_shortlinks:
		try:
			print (urllib2.urlopen(link).url)
		except urllib2.HTTPError as e:
			print ('\t', e)
