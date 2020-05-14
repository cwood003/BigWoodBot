# in order to build this module I referenced shalvah's @this_vid tweet_operations
import tweepy
import logging
import json
import time
import types
from operator import itemgetter
from API import create_api, at_name
from utils import Error, get_json_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def filter_video(variants):
    video_variant = "video/mp4"
    filtered_variants = []
    for variant in variants:
        if variant["content_type"] == "video/mp4":
            filtered_variants.append(variant)

    return max(filtered_variants, key=itemgetter("bitrate"))


def look_for_link(object):
    links = []
    for key in object.keys():
        if isinstance(object[key], str) and object[key].startswith('http'):
            links.append(object[key])
        elif isinstance(object[key], dict):
            nested_link = look_for_link(object[key])
            if nested_link:
                return nested_link
    return links


def get_video_link(api, status_json):
    try:
        media_variants = status_json["extended_entities"]["media"][0]["video_info"]["variants"]
        return filter_video(media_variants)['url']
    except:
        try:
            additional_media_info = status_json["extended_entities"]["media"][0]["additional_media_info"]
            additional_media_info['embeddable']

            if additional_media_info and additional_media_info['embeddable'] is None:
                # look for link
                link = look_for_link(additional_media_info)
                if not link:
                    return Error(1, 'Error')
                return Error(2, link)
            elif status_json['entities']['media']:
                # tweet is share of another tweet containing media
                expanded_url = status_json['entities']['media'][0]['expanded_url'].split('/')
                tweetId = expanded_url[len(expanded_url) - 3]
                if tweetId != status_json['id']:
                    ogTweet = api.get_status(tweetId)
                    ogTweet_json = get_json_dict(ogTweet)
                    return get_video_link(api, ogTweet_json)
        except:
            return Error(3, "##")


def is_error(error):
    if isinstance(error, Error):
        return True


# call get_video_link and
def send_image(api, status_json, child_status_json):
    link = get_video_link(api, status_json)
    try:
        api.send_direct_message(child_status_json["user"]["id"], link.message)
        if link.error_code == 2:
            api.send_direct_message(child_status_json["user"]["id"], link.link)
    except:
        api.send_direct_message(child_status_json["user"]["id"], "Here is the link to your video slick: " + link)
