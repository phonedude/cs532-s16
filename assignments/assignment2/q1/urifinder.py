# -*- encoding: utf-8 -*-
import requests
from requests_oauthlib import OAuth1
from urllib import quote

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "c7VFfCTtUqFDg69MRHvGnpSwt"
CONSUMER_SECRET = "4r8yeBQmziO8HuXY3UQN3qGigz0hgrbQxXpD4w2nR7fBRIRLqU"

OAUTH_TOKEN = "798668178-bH8DbMpNuWkfhAHxuODgWSHwQE65B1WZnc4Ahtej"
OAUTH_TOKEN_SECRET = "FhykPKnQcgKQBE43os2bDZ31ugH9RVSG3HYoOL7QG7RNC"

SEARCH_URI = "https://api.twitter.com/1.1/search/tweets.json?q="

SEARCH_ITEMS = map(quote, [ 'allu arjun', 
							'vijayawada', 
							'Cristiano Ronaldo', 
							'Adolf Hitler', 
							'Emma Watson', 
							'Anushka Shetty', 
							'Rajini Kanth',
							'Lionel Messi',
							'Ricardo Kaka',
							'Wayne Rooney',
							'Gareth Bale',
							'Neymar',
							'Malaika Arora Khan',
							'Isco',
							'Adam Gilchrist',
							'Kevin de bruyne',
							'Kevin Pietersen',
							'Julia Roberts',
							'Scarlett Johansson',
							'Kate Winslate',
							'Kamal Hassan',
							'Kumar sangakkara'
							'Mahela jayawardene'
							'Roger Federer'
							'Maria Sharapova'
							'Serena Williams'
							'Venus Williams'
							'Justin Henin'
							'Justin Langer'
							'Sania Mirza'
							'Shoaib Malik'
							'Shoaib Aktar'
							'Sourav Ganguly'
							'Rafeal Nadal'
							'Real Madrid CF'
							'Rahul Dravid'
							'Manchester United'
							'FC Barcelona '
							'Manchester City'
							'Chelsea FC'
							'Liverpool FC'
							'Aston Villa FC'
							'Aston Martin'
							'lamborghini'
							'FC Bayern Munich'
							'Borussia Dortmund'
							'Philipp Lahm'
							'Sergio Ramos'
							'Sergio Aguero'
							'Marcelo Vieira'
							'Luis Suarez'
							'Luis Enrique'
							'Jose Mourinho'
							'Alex Ferguson'
							'Pep Guardiola'
							'Shane Watson'
							'Shane Warne'
							'Bill Gates'
							'Rothschild'
							'Mark Zuckerberg'
							'Chetan Bhagat'
							'Ishant Sharma'
							'Virat Kohli'
							'Sachin Tendulkar'
							'Ricky Ponting'
							'Matthew Hayden'
							'Rohit Sharma'
							'Irfan Pathan'
							'yusuf Pathan'
							'Katrina Kaif'
							'Anushka Sharma'
							'Salman Khan'
							'Ranbir Kapoor'
							'Puneeth Rajkumar'
							'Rajkumar'
							'Ganesh'
							'Upendra'
							'Darshan'
							'Shivrajkumar'
							'Rakhul Preeth Singh'
							'Soundarya'
							'Savitramma'
							'Anusuya'
							'Roja'
							'Ram Gopal Varma'
							'Pawn Kalyan'
							'Ram Charan'
							'Allu Arvind'
							'Allu Ramalinga'
							'Kotta Srinivas Rao'
							'Surya'
							'Joythika'
							'Nagarjun'
							'Akhil Akkeneni'
							'Naga Chaitanya Akkeneni'
							'Amala Akkeneni'
							'Barack Obama'
							'Abdul Kalam'
							'Subhash Chandra Bose'
							'Shreya Ghoshal'
							'Shreya Sharan'
							'Sidharth'
							'Mahesh Babu'
							'Jenelia '
							'Salam Khan'
							'Sharukh Khan'
							'Hrithik Roshan'
							'Deepika Padukone'
							'Pooja Ghandhi'
							'Ravichandranan'
							'Arjun Sarja'
							'Shankar Nag'
							'Prakash Raj'
							'Tennis Krishna'
							'Nagesh'
							'Lokanath'
							'Meena'
							'Arundathi Nag'
							'Nagma'
							'Laila Mehdin'
							'Sindhu Menon'
							'Jaylalithaa'
							'Vishnuvardhan'
							'Suman Nagarkar'])

def get_oauth():
	return OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)

def find_uris(uris):
	with open('output', 'a') as outfile:
		for search_item in SEARCH_ITEMS:
			result = requests.get(SEARCH_URI + search_item + '&filter%3Alinks&count=10000', auth=oauth)
			for status in result.json()['statuses']:
				for url in status['entities']['urls']:
					if len(uris) == 10000:
						return
					if 'expanded_url' in url:
						try:
							result = requests.get(url['expanded_url'], timeout=4)
							# only add expanded uris if they aren't in the list already
							if result.status_code == 200 and result.url not in uris:
								add_uri(uris, result.url)
								outfile.write('%s\n' % result.url)
						except Exception as e:
							print e
							continue

def add_uri(uris, uri):
	uris.add(uri)
	print 'added uri #%d: %s' % (len(uris), uri)

if __name__ == "__main__":
	oauth = get_oauth()
	uris = set()
	# read in previous set of uris
	try:
		with open('output', 'r') as infile:
			for line in infile.readlines():
				add_uri(uris, line.strip())
	except IOError:
		pass
	find_uris(uris)