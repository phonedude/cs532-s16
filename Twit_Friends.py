# -*- coding: utf-8 -*-
import tweepy
import os
import simplejson as json
import time

dir = r'F:\Web_Science\cs532-s16\A4'
os.chdir(dir)

auth = tweepy.OAuthHandler('Vz8rTepvf3kVJ2Php7wcIypNt',
                           'mnkqCLchG38kZEgN36Vlub8o5bmwRD0CLTGNdNlDxaGxiBb7K0')
auth.set_access_token('4625770576-Ok6PkaV9hzc6I4kR1jb6Qd48QjYCZvlRhrzYTVu',
                      '5mWFt5p12bgANFYAe7rjXv4jHH55Ekv5eGwaprEFyqfer')


api = tweepy.API(auth)
f = open("twit.csv","a")
#t = api.get_user ("phonedude_mln")
f.write("Followers\n")
for follower in tweepy.Cursor(api.followers,id="phonedude_mln",items=10).items(200):
    f.write("%s\n"%follower.followers_count)
    time.sleep(.5)