import tweepy
from tweepy import OAuthHandler
import time

# Authentication details. To  obtain these visit dev.twitter.com
access_token = "XXXXXX"
access_token_secret = "XXXXXX"
consumer_key = "XXXXXX"
consumer_secret = "XXXXXX"

if __name__ == '__main__':
    # Create authentication token
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    data = api.get_user('phonedude_mln')
    print 'Followers: ' + str(data.followers_count)
    
    for user in tweepy.Cursor(api.followers, screen_name="phonedude_mln", count = 200).items():
		print user.screen_name, user.followers_count
