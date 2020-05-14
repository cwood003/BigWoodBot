# Cole Wood starting 12/18/2019

import tweepy
import datetime
#year month day hour minute second microsecond tzinfo
# Authenticate to Twitter
auth = tweepy.OAuthHandler("pjkCfbqKMKSL0i3kHMmvOn63I","QskpiTQaH8OMNwdvs5CgtKJGhlxcEbLuUH3ntQWtgcLlGqMrBV")
# the_young_wood
#auth.set_access_token("2607279628-x37IxROK0K2n9lqfu0v1LOXBBNCzLs8muYUsVIS", "bWjf6BpWnipw7sLCMcPm5929YFDiFs6IY5brD2ochRXbe")

# Mcaffee Bot
auth.set_access_token("1207470907381501959-7o8ufhVG7uQTsjsqfDb0tgfV8rbXV1", "sPn2u7AIoOXmHSBeiBU3k7yjUjAhLCiL6irAm8YTH266Z")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication Okay!")
except:
    print("Error, something went wrong big guy")

#api.update_status("#BarstoolBestBar #BarstoolJJs")

arkWords = "#BarstoolJJs", "#BarstoolBestBar"
ndWords = "#BarstoolJoeBlacks", "#BarstoolBestBar"
sinceWhen = "2020-03-24"
time1 = datetime.datetime(2020, 3, 24, 11, 0, 0)

JJs = tweepy.Cursor(api.search, q=arkWords, since=sinceWhen).items()

JBs = tweepy.Cursor(api.search, q=ndWords, since=sinceWhen).items()

arkVotes = []
arkVotesNotFiltered = list(JJs)

ndVotes = []
ndVotesNotFiltered = list(JBs)

for tweet in arkVotesNotFiltered:
    #print("----------------------------------------------------------")
    #print(f"{tweet.user.name} said {tweet.text} at {tweet.created_at}")
    try:
        print("Retweeted: " + tweet.retweeted_status.user.name)
    except:
        print("Not Retweeted")
        if tweet.created_at > time1:
            arkVotes.append(tweet.user.id)

for tweet in ndVotesNotFiltered:
    try:
        print("Retweeted: " + tweet.retweeted_status.user.name)
    except:
        #print("Not Retweeted")
        if tweet.created_at > time1:
            ndVotes.append(tweet.user.id)

uniqueArk = []
uniqueND = []
for vote in arkVotes:
    if vote not in uniqueArk:
        uniqueArk.append(vote)

for vote in ndVotes:
    if vote not in uniqueND:
        uniqueND.append(vote)

print("Arky not filtered:")
print(len(arkVotesNotFiltered))
print("Ark votes filtered RTs including dupes:")
print(len(arkVotes))
print("Unique Arky:")
print(len(uniqueArk))

print("ND not filtered:")
print(len(ndVotesNotFiltered))
print("ND votes filtered RTs including dupes:")
print(len(ndVotes))
print("Unique ND:")
print(len(uniqueND))

