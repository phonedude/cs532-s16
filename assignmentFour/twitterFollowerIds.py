import time
import tweepy

auth = tweepy.OAuthHandler("38wZKZuUuwGitHkE3dMpR7jEz", "czTV2ryAOTlep7FPC8dVsaAwS28Cw8Z7L8gDCLnj22ioo0uyuG")
auth.set_access_token("2352884547-xheIpcHT0oIjJmzGUkIHwt5X2IZmwogTMh9YWvc", "70RS08peFisvJyPOZGlPleQqfg98twYVkIQefeEP1Ifdg")

outputFile = open("twitterFollowerAmt.txt", 'w')
idFile = open("twitterFollowerIds.txt", 'w')

counter = 1
api = tweepy.API(auth)

ids = []

for page in tweepy.Cursor(api.followers_ids, screen_name="JuicyJake1868").pages():
    ids.extend(page)
    time.sleep(5)

print len(ids)

for name in ids:
    print name
    user = api.get_user(name)
    print user.followers_count
    outputFile.write(str(counter) + "           " + str(user.followers_count))
    outputFile.write("\n")
    print name
    idFile.write(str(name))
    idFile.write("\n")
    counter += 1

idFile.close()
outputFile.close()




