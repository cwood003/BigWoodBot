import tweepy
import logging
import json
import time
from API import create_api, at_name
from send_image import send_image
from utils import send_error_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# switcher function if when we get more functions
def function(argument, api, status_json, child_status_json, me):
    switcher = {
        'dwn': send_image
    }
    try:
        # returns valid command
        return switcher[argument](api, status_json, child_status_json)
    except KeyError:
        # tells user they didn't use valid command
        return send_error_message(api, argument, child_status_json)


# mention listener just waiting for out @bigwood_bot
class MentionListener(tweepy.StreamListener):
    # we never really us me so maybe we remove it?
    def __init__(self, api, keyword):
        self.api = api
        self.me = api.me()
        self.keyword = keyword
    # method that proc on status with our keyword
    def on_status(self, status):
        logger.info(f"Processing tweet id {status.id}")
        # ignore if retweeted
        if status.retweeted:
            logger.info("Retweeted")
            return

        # get child tweets json info from tweet
        child_json_string = json.dumps(status._json)
        child_status_json = json.loads(child_json_string)

        # where I put approval list check and return
        # here

        # get parent json info from child tweet
        parent_json_string = json.dumps(
            self.api.get_status(child_status_json["in_reply_to_status_id"], tweet_mode='extended')._json)
        parent_status_json = json.loads(parent_json_string)

        # getting arguments from tweet text
        unordered_args = list()
        temp = str(child_status_json["text"]).split(" ")
        # filtering out spaces from the list
        for item in temp:
            if item is not " " and item is not '':
                unordered_args.append(item)
        # make sure arguments only count after @bigwood_bot
        args = []
        screen_name_position = unordered_args.index("@" + self.keyword)
        first_arg = screen_name_position + 1
        second_arg = screen_name_position + 2
        print(screen_name_position)
        index = screen_name_position + 1
        flag = False
        for token in unordered_args:
            if flag:
                args.append(token)
            if token == "@" + self.keyword:
                flag = True

        # potentially add more than one
        if len(args) > 0:
            logger.info("Sending Image")
            function(args[0], self.api, parent_status_json, child_status_json, self.me)


def main(keyword):
    api = create_api()
    mention_listener = MentionListener(api, at_name)
    stream = tweepy.Stream(api.auth, mention_listener)
    stream.filter(track=[keyword])


if __name__ == '__main__':
    main(at_name)
