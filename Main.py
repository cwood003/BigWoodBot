# Cole Wood starting 12/18/2019

import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("pjkCfbqKMKSL0i3kHMmvOn63I","QskpiTQaH8OMNwdvs5CgtKJGhlxcEbLuUH3ntQWtgcLlGqMrBV")
# the_young_wood
#auth.set_access_token("2607279628-x37IxROK0K2n9lqfu0v1LOXBBNCzLs8muYUsVIS", "bWjf6BpWnipw7sLCMcPm5929YFDiFs6IY5brD2ochRXbe")

# Big Wood Bot
auth.set_access_token("1207470907381501959-7o8ufhVG7uQTsjsqfDb0tgfV8rbXV1", "sPn2u7AIoOXmHSBeiBU3k7yjUjAhLCiL6irAm8YTH266Z")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Aunthentication Okay!")
except:
    print("Error, something went wrong big guy")

api.update_status("Test 1")

