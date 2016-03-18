import time
import tweepy
import json
import sys
import os
import re

consumer_key = "mvW9Y4uy8xJWMNwqV97qCa2aX"
consumer_secret = "vyCabSoD6CPXeAdL7onyEGO6lBl6YyPeivLpng1MgM2bOBjisU"
access_token = "798668178-bH8DbMpNuWkfhAHxuODgWSHwQE65B1WZnc4Ahtej"
access_token_secret = "FhykPKnQcgKQBE43os2bDZ31ugH9RVSG3HYoOL7QG7RNC"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
screen_name='9ulovesu'

try:
    user = api.get_user(screen_name)
except tweepy.TweepError as e:
    if isinstance(e, tweepy.TweepError):
		print('RateLimitError')

    sys.exit(1)
	
print(user.screen_name,user.id)
ids = [f for f in user.followers_ids()]

ids.append(user.id)
user_friends = {}
print(user.followers_count, ids)

counter = 0
excluded = []

for id_ in ids:
	friend = api.get_user(id_)
	print(counter, friend.name, friend.profile_image_url, friend.id)
	print '-->'
	counter += 1
	user_connected_friends = []
	
	try:
		friend_followers = [f for f in api.get_user(friend.id).followers_ids()]
		for connected in friend_followers:
			if connected in ids:
				print(connected )
				print(",")
				user_connected_friends.append(connected)
		user_friends[friend.id] = {'name':friend.name, 'avatar':friend.profile_image_url, 'screen_name': friend.screen_name, 'followers_count': friend.followers_count, 'friends_count':friend.friends_count, 'connected_to': user_connected_friends}
		print(user_friends[friend.id])
	except tweepy.TweepError as e:
		print('\n This is ---', e)
		if isinstance(e, tweepy.TweepError):
			time.sleep(60 * 15)
			try:
				friend_followers = [f for f in api.get_user(friend.id).followers_ids()]
				for connected in friend_followers:
					if connected in ids:
						print(connected)
						print(",")
						user_connected_friends.append(connected)
				user_friends[friend.id] = {'name':friend.name, 'avatar':friend.profile_image_url, 'screen_name': friend.screen_name, 'followers_count': friend.followers_count, 'friends_count':friend.friends_count, 'connected_to': user_connected_friends}
				print(user_friends[friend.id])
				continue
				
			except tweepy.TweepError as e:
				print(e)
				excluded.append(friend.id)
		else:
			print(e)
			excluded.append(friend.id)

with open("9ulovesu.json", 'w') as file:
    data = json.load(file)