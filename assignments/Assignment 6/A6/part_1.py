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

    #for user in tweepy.Cursor(api.followers, screen_name="AtHeartEngineer", count = 200).items():
    	#print user.screen_name

    people = []
    followers = []
    with open('tylers_followers.txt') as f:
    	for line in f:

    		followers.append(line)

    with open('temp.txt') as g:
    	for line in g:
    		people.append(line)

    for person in people:
    	for follower in followers:
    		if person == follower:
    			pass
    		else:
    			relationship = api.show_friendship(source_screen_name=person, target_screen_name=follower, count=200)
    			source, target = relationship
    			print str(source.followed_by) + " " + target.screen_name
    			print str(target.followed_by) + " " + source.screen_name
    			print "\n"
