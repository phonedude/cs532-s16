#! /usr/bin/python

import requests
import concurrent.futures
import md5
from bs4 import BeautifulSoup
import pickle

def convert(uri):
	return md5.new(uri).hexdigest()

def get_html(uri):
	print('Getting {}'.format(uri))
	response = requests.get(uri)
	return response.url, response.status_code, response.content

if __name__ == '__main__':
	with open('links') as infile:
		uris = [uri.rstrip('\n') for uri in infile]

	with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
		uri_futures = [executor.submit(get_html, uri) for uri in uris]
		for future in concurrent.futures.as_completed(uri_futures):
			try:
				uri, status_code, content = future.result()
			except Exception as exc:
				print('{} generated an exception: {}'.format(uri, exc))
				continue
			if status_code == 200:
				hashed_uri = convert(uri)
				print('Writing {} as {}'.format(uri, hashed_uri))
				try:
					with open('html/raw/' + hashed_uri, 'w') as outfile:
						outfile.write(uri + '\n')
						outfile.write(content)
					with open('html/processed/' + hashed_uri + '.processed.txt', 'w') as outfile:
						outfile.write(uri + '\n')
						outfile.write(BeautifulSoup(content).get_text().encode('utf8'))
				except Exception as e:
					print '**** ERROR **** --- ' + uri
					print e
			else:
				print('Not writing {}, bad status code: {}'.format(uri, status_code))
