#!/usr/bin/env python3
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
import re

# this code was adapted from the example found at
# https://gist.github.com/bonzanini/af0463b927433c73784d


# this regex was used to extract un-expanded urls before thinking smart was an idea
reg = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.VERBOSE | re.IGNORECASE)


def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    return parser

# Subclass StreamListener so that I can handle the data
# Normally the StreamListener simply consumes and does nothing
# You must subclass for anything to happen
class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, query):
        query_fname = format_filename(query)
        self.outfile = "urls%s.dat" %  query_fname
        useragent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.01'
        # self.outfile = "%s/stream_%s.json" % (data_dir, query_fname)

    # when there is a tweet simply append the extracted urls to a file
    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                map = json.loads(data)
                #I found in the json data that there is an expanded_url portion
                #Which unshortens one level
                #Even then some shortened uris get shortened
                for it in map['entities']['urls']:
                        f.write("%s\n"%it['expanded_url'])

                return True
        except BaseException as e:
            #if bad data just let me know and move on
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(fname):
    """Convert file name into a safe string.
    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    args = parser.parse_args()
    #set up oauth
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    # open a stream up and give it my listener
    twitter_stream = Stream(auth, MyListener(args.query))
    # filter the open stream for the query
    # this looks for recent tweets only
    twitter_stream.filter(track=[args.query])
