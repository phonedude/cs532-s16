import time
import tweepy

consumer_key = "KEtYeXDYJwgdtX0IHuwUf1Hsw"
consumer_secret = "xkErPgMDfParcniEkbhRLgf8T6EXGOfhNP1bAbKSbog5rqCKxi"
access_key = "308651543-bWKmgqe2AP3xTx85jyHPBUrovjdMtNej2SOqOjZd"
access_secret = "PgKsQJxjvqaocAZmNG2D5t2Q7ZkAcDoPTHvLfOEe2ghj9"

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_key,access_secret)

api = tweepy.API(auth)

user = api.get_user('amrali70')

print "Number of Followers I have is = " + "{0}".format(user.followers_count)

ids = []
i = 0
for user in tweepy.Cursor(api.followers, screen_name="amrali70", count=1000).items():
    try:
      i = i+1	
      name = api.get_user(user.screen_name)
      with open('detailsfollowers.txt','a') as f:
        line = "Number of Followers "+ user.screen_name + " have is = " + "{0}".format(name.followers_count) + '\n'
        f.write(line)	  
      print "Number of Followers "+ user.screen_name + " have is = " + "{0}".format(name.followers_count)
      if((i%50) == 0):
        print i
      if(i==299):
        time.sleep(60*15)
    except:
        print "waiting"
        time.sleep(10)	
print "Number of Followers" + "{0}".format(i)