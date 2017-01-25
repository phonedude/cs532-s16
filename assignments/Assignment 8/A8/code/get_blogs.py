import tweepy
from tweepy import OAuthHandler

access_token = "XXXXXX"
access_token_secret = "XXXXXX"
consumer_key = "XXXXXX"
consumer_secret = "XXXXXX"

if __name__ == '__main__':

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	search_results = api.search(q="my%20blog", count=250)
	users = []
	blogs = []
	i = 0

	for tweet in search_results:
			if tweet.user.screen_name in users:
				next
			else:
				users.append(tweet.user.screen_name)

	for user in users:
		data = api.get_user(user)
		if (data.url != None):
			if data.url in blogs:
				next
			else:
				blogs.append(data.url)
				print data.url
				
