import tweepy
from tweepy import OAuthHandler
import time
import requests

access_token = "XXXXXX"
access_token_secret = "XXXXXX"
consumer_key = "XXXXXX"
consumer_secret = "XXXXXX"

if __name__ == '__main__':

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	with open('tylers_followers.txt') as f:
		for line in f:
			user = line.strip()
			real_name = api.get_user(screen_name=user)
			print (user, real_name)
