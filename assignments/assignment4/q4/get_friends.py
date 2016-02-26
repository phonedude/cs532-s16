# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import re 
import os
import sys
import json
import requests
import subprocess
from urlparse import parse_qs
from requests_oauthlib import OAuth1

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "lA3ACTYCPDE8G5rNYFBMI1hMm"
CONSUMER_SECRET = "4zGZNDRA2m32dsq7nCMfwJojGSanz6ohgf4ZaNWKDxCaabPUai"
OAUTH_TOKEN = "798668178-bH8DbMpNuWkfhAHxuODgWSHwQE65B1WZnc4Ahtej"
OAUTH_TOKEN_SECRET = "FhykPKnQcgKQBE43os2bDZ31ugH9RVSG3HYoOL7QG7RNC"

def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print
    else:
		twitterUser = "phonedude_mln"

		print 'Searching Twitter for following counts of '+twitterUser+"'s following: "
		oauth = get_oauth() 

		print '%-15s %-20s' %('Friends_count','Friends-screen-name')			
		
		# initial reading from the twitter account where cursor = -1 (e.g. first page)
		r = requests.get(url="https://api.twitter.com/1.1/friends/list.json?cursor=-1&count=2000&screen_name="+twitterUser+"&skip_status=true&include_user_entities=false", auth=oauth)
		counter = 0
		res = r.json()
		while True:
			raw_res = res['users']
			for init_url in raw_res:
				counter = counter + 1
				print '%-15d %-20s' %(init_url['friends_count'],init_url['screen_name'].encode('ascii', 'replace'))
				with open('friend_counts', 'a') as outfile:
				    outfile.write('%-15d %-20s\n' %(init_url['friends_count'],init_url['screen_name'].encode('ascii', 'replace')))
			if str(res['next_cursor']) == '0':
				break
			else:
				r = requests.get(url="https://api.twitter.com/1.1/friends/list.json?cursor="+str(res['next_cursor'])+"&count=100&screen_name="+twitterUser+"&skip_status=true&include_user_entities=false", auth=oauth)
				res = r.json()
	
print '\nNumber of '+twitterUser+"'s friends is: "+str(counter)