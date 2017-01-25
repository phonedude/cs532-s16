import csv
import json

import networkx as nx
import tweepy

import config


# get the friends for a person
def getFriends(api, screenname):
    print("looking up friends for follower: %s\n" % screenname)
    fl = []
    # get the friends by using a cursor to query the twitter api
    items = {'screenname': screenname}
    try:
        for friend in tweepy.Cursor(api.friends, screen_name=screenname, count=200).items():
            fl.append(friend.screen_name)
    except Exception as e:
        print("There was an exception ", e)
    items['friends'] = fl
    with open("wsdlfollwerFriends.json", "a") as out:
        out.write(json.dumps(items, indent=2) + ",\n")
    return fl



# get the wsdl groups twitter followers
def getWSDL_follwers(tapi):
    fs = []  # type: list[tweepy.User]
    # get the followers by using a cursor to query the twitter api
    for page in tweepy.Cursor(tapi.followers, screen_name="WebSciDL", count=200).pages():
        print(page)
        fs.extend(page)

        # add the followers to out dic
    with open("wsdltwitterfollwers.csv", "w+") as out:
        out.write("name,screenName,imurl\n")
        for pp in fs:
            print(pp)
            out.write("%s,%s,%s\n" % (pp.name, pp.screen_name, pp.profile_image_url))


def get_friends():
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    # do not want twitter to slap a rate limit exceeded on me so explicitly wait after each request to avoid that
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)  # type: tweepy.API
    with open("wsdlfollwerFriends.json", "r+") as r:
        it = json.load(r)
        print(it)
    gotten = set(map(lambda x: x['screenname'], it['followers']))
    for g in gotten:
        print(g)

    with open('wsdltwitterfollwers.csv', "r") as o:
        reader = csv.DictReader(o)
        out = {}
        for row in reader:
            print(row)
            if row['screenName'] not in gotten:
                print(row['screenName'])
                flist = getFriends(api=api, screenname=row['screenName'])
                if len(flist) > 0:
                    print(len(flist))



if __name__ == "__main__":
    print("Hi")
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    # do not want twitter to slap a rate limit exceeded on me so explicitly wait after each request to avoid that
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)  # type: tweepy.API
    # # build_graph()
    # # tweepy.User
    # bg2()

    getWSDL_follwers(api)
    get_friends()
    # set up oauth
