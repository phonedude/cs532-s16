# -*- coding: utf-8 -*-
import tweepy
import requests


auth = tweepy.OAuthHandler('Vz8rTepvf3kVJ2Php7wcIypNt',
                           'mnkqCLchG38kZEgN36Vlub8o5bmwRD0CLTGNdNlDxaGxiBb7K0')
auth.set_access_token('4625770576-Ok6PkaV9hzc6I4kR1jb6Qd48QjYCZvlRhrzYTVu',
                      '5mWFt5p12bgANFYAe7rjXv4jHH55Ekv5eGwaprEFyqfer')


api = tweepy.API(auth)

links = []

f = open("F:\Web_Science\cs532-s16\Assignment2\links.txt", "a")

for status in tweepy.Cursor(api.user_timeline,id = '@NRA',include_entities=True).items():
    for url in status.entities['urls']:
        expanded_url = url['expanded_url']
        r= requests.head(expanded_url)
        if len(links) in range (0,1000): 
            if r.status_code in range (200,300):
                l = str((format(r.url)))
                if links.count(l) == 0:
                    links.append (l)
            elif r.status_code in range (300,400):
                l = str((format(r.headers['location'])))
                if links.count(l) == 0:
                    links.append (l)
            else:
                print (format(r.status_code))
        else:
            for item in links:
               #print (item)
               f.write(item + '\n')
               
f.close                