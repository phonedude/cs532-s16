#!/usr/bin/env python3
import tweepy
import config


def mlnfollowers(api):
    fs = []
    it = {}
    # get the followers by using a cursor to query the twitter api
    for page in tweepy.Cursor(api.followers, screen_name="phonedude_mln", count=200).pages():
        print(page)
        fs.extend(page)

    # add the followers to out dic
    for pp in fs:
        it[pp.screen_name] = pp.followers_count
        print(pp.screen_name, pp.followers_count)

    # add our glorious leader
    it["phonedude_mln"] = str(len(fs))

    # write it out to a file
    with open("mlntwfollowers.csv", "w+") as out:
        out.write("following,count\n")
        for k, v in it.items():
            out.write("%s,%s\n" % (str(k), str(v)))


def mlnfollowing(api):
    fs = []
    it = {}
    # get the friends by using a cursor to query the twitter api
    for page in tweepy.Cursor(api.friends, screen_name="phonedude_mln", count=200).pages():
        print(page)
        fs.extend(page)

    # add the friends to out dic
    for pp in fs:
        it[pp.screen_name] = pp.followers_count
        print(pp.screen_name, pp.followers_count)

    # add our glorious leader
    it["phonedude_mln"] = str(len(fs))

    # write it out to a file
    with open("mlntwfollowing.csv", "w+") as out:
        out.write("following,count\n")
        for k, v in it.items():
            out.write("%s,%s\n" % (str(k), str(v)))


if __name__ == '__main__':
    # set up oauth
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    # do not want twitter to slap a rate limit exceeded on me so explicitly wait after each request to avoid that
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)  # type: tweepy.API

    mlnfollowing(api)

    mlnfollowers(api)
