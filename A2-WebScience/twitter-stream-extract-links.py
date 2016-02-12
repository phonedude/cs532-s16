from twitter import *
# Tarek Fouda
# This program prints 1000 URLs in my twitter news feed
# using twitter API package downloaded from GITHUB.
config = {}
execfile("config.py", config)
auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"])
stream = TwitterStream(auth = auth, secure = True)
tweet_iter = stream.statuses.filter(track = "social")
listCount = 1
textCount = 1
l = []
for tweet in tweet_iter:
	if (textCount<=1000):
		for url in tweet["entities"]["urls"]:
			try:
				l.insert(listCount,url["expanded_url"])
				if (l.count(url["expanded_url"])<= 1):
					print "Found URL: %s" % url["expanded_url"]
					f = open('urls.txt','a')
					f.write(url["expanded_url"] +'\n')
					textCount = textCount +1
					f.close()
				else:
					pass
			except:
				print "except"
		listCount = listCount+1		
	else:
		break