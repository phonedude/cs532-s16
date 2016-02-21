import re
import sys
import os
import requests
import validators
import urllib3

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from lib.WEBlib import AddURI
from TwitterSearch import *

__author__ = 'Plinio H. Vargas'
__date__ = 'Wed,  Feb 03, 2016 at 22:27:02'
__email__ = 'pvargas@cs.odu.edu'

"""
Given a set of key words this program makes use of TwitterSearch API to search for any tweets
related to the key words, and then extract the URI within in the tweet.
"""
root_url_array = []
all_links_set = set()
final_link = ''


def add_links(ts, key_words):
    global final_link
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords(key_words) # let's define all words we would like to have a look for
        tso.set_language('en') # we want to see English tweets only
        tso.set_include_entities(False) # and don't give us all those entity information

         # get all tweet feeds with parameter above
        for tweet in ts.search_tweets_iterable(tso):
            if len(all_links_set) >= 1000:
                break

            tweet_text = tweet['text']

            # extract url from tweet
            url = re.findall(r'(https?://[^\s]+)', tweet['text'])

            # analyze url
            for uri in url:

                # check if url has been already used
                if uri not in root_url_array:
                    root_url_array.append(uri)

                    if validators.url(uri):
                        AddURI(all_links_set, uri)

    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)

    return

# it's about time to create a TwitterSearch object with our secret tokens
ts = TwitterSearch(
    consumer_key='consumerkey',
    consumer_secret='consumersecrete',
    access_token='access_token',
    access_token_secret='accesstokensecret'
)

# find tweets for a particular key word
with open('keywords.txt', 'r') as file:
    for record in file:
        keys = record.strip().split(',')

        key_words = []
        for words in keys:
            key_words.append(words.strip())

        add_links(ts, key_words)
        print(len(all_links_set))

# save unique URIs to a file
with open('linkfiles.txt', 'w') as out:
    for link in all_links_set:
        out.write(link + '\n')
