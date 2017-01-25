from sets import Set
from ttp import ttp
from ttp import utils
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import unicodedata
import urllib

access_token = "XXXXXXX"
access_token_secret = "XXXXXXX"
consumer_key = "XXXXXXX"
consumer_secret = "XXXXXXX"

unique_links = Set()

class StdOutListener(StreamListener):
	def on_data(self, data):
		global unique_links
		# get the text from the tweet
		json_dict = json.loads(data)
		
		if 'text' not in json_dict:
			return True
		text = unicodedata.normalize('NFKD', json.loads(data)['text']).encode('ascii','ignore')
		parsed = ttp.Parser().parse(text)
		urls = parsed.urls
		# check if urls is empty and return immediately
		if not urls:
			return True

		# long_urls returns a dictionary of short_url to list[short_url, long_url]
		long_urls = utils.follow_shortlinks(urls)
		for url in urls:
			# use a regex to pull the link from the text
			links = long_urls[url]
			if links is not None:
				# long urls returns a dictionary with a list of each url - take the last one
				link = links[-1]
				# the link is real - now need to get the link address
				resp = urllib.urlopen(link)
				if resp.getcode() == 200:		
					# add the long link to our unique links, or cancel if there's already 1000
					if len(unique_links) < 1000:
						if link not in unique_links:
							print link
						unique_links.add(link)
						return True
					else:
						return False

	def on_error(self, status):
		pass

if __name__ == '__main__':
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream_listener = StdOutListener()
	stream = Stream(auth, stream_listener)
	stream.filter(locations=[-180,-90,180,90], async=True)