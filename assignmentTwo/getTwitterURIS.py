from twitter import *
from urlparse import urlparse

unsortedFileName = 'UnsortedURL.txt'

con_secret = "38wZKZuUuwGitHkE3dMpR7jEz"
con_secret_key = "czTV2ryAOTlep7FPC8dVsaAwS28Cw8Z7L8gDCLnj22ioo0uyuG"

token = "2352884547-xheIpcHT0oIjJmzGUkIHwt5X2IZmwogTMh9YWvc"
token_key = "70RS08peFisvJyPOZGlPleQqfg98twYVkIQefeEP1Ifdg"

unsortedFile = open(unsortedFileName, 'a') #Opens the unsorted file

t = Twitter(
    auth=OAuth(token, token_key, con_secret, con_secret_key))

# Get your "home" timeline
x = t.statuses.home_timeline()
#x = t.statuses.user_timeline(screen_name="timoreilly")


twitter_stream = TwitterStream(auth=OAuth(token, token_key, con_secret, con_secret_key))
iterator = twitter_stream.statuses.sample()
counter = 0

for tweet in iterator:
    if 'entities' in tweet:
        for url in tweet['entities']['urls']:
            unsortedFile.write(url['expanded_url']) 
            unsortedFile.write("\n")
            #print url['expanded_url']
            print counter
            counter = counter + 1
            if counter == 1000:
			    break
    if counter == 1000:
	    break

with open('SortedLinks.txt') as f:
    lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

for urls in lines:
    
    print urls

unsortedFile.close() 
	 