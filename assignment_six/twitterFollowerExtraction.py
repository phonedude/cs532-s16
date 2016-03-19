import tweepy
import time 

idFile = open("twitterFollowerIds.txt", 'w')
fileNumberAndId = open("twitterFollowerNums.txt", 'w')
outputFile = open("twitterOutput.txt", 'w')

auth = tweepy.OAuthHandler("38wZKZuUuwGitHkE3dMpR7jEz", "czTV2ryAOTlep7FPC8dVsaAwS28Cw8Z7L8gDCLnj22ioo0uyuG")
auth.set_access_token("2352884547-xheIpcHT0oIjJmzGUkIHwt5X2IZmwogTMh9YWvc", "70RS08peFisvJyPOZGlPleQqfg98twYVkIQefeEP1Ifdg")
api = tweepy.API(auth, wait_on_rate_limit=True)

#friends = api.friends_ids(api.me().id)
print("You follow", len(friends), "users")
matchCounter = 0
print api.me().id
for follower in tweepy.Cursor(api.followers).items():
    print("Follower name: ", str(follower.screen_name))
    idFile.write(str(follower.id) + "           " + str(follower.screen_name))
    idFile.write("\n")
    fileNumberAndId.write(str(follower.id))
    fileNumberAndId.write("\n")

fileNumberAndId.close()
idFile.close()
with open('twitterFollowerNums.txt') as f: 
    lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

with open('twitterNumbers.txt') as z: 
    nums = z.readlines()
    nums = [p.strip('\n') for p in nums]

for twIds in lines:
    outputFile.write("for Id: " + str(twIds))
    outputFile.write("\n")
    try:
        for friendList in tweepy.Cursor(api.followers_ids, twIds).items():
            for secondList in lines:
                if str(secondList) == str(friendList):
                    print "Hit!"
                    outputFile.write("hit from: " + str(friendList) + "  equals " + str(secondList))
                    outputFile.write("\n")
        print "next follower!"
    except tweepy.TweepError as e:
        time.sleep(900)
    	for friendList in tweepy.Cursor(api.followers_ids, twIds).items():
            for secondList in lines:
                if str(secondList) == str(friendList):
                    print "Hit!"
                    outputFile.write("hit from: " + str(friendList) + "  equals " + str(secondList))
                    outputFile.write("\n")
        print "next follower! (after timeout)"
outputFile.close()