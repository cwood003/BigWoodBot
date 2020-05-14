import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# error message switcher class
class Error:
    def __init__(self, error_code, link):
        message1 = "This video is possibly from an external publisher who has restricted it. It cannot be accessed."
        message2 = "Tweet is restricted but we might be able to get link."
        message3 = "No video in the tweet."

        switcher = {
            1: message1,
            2: message2,
            3: message3
        }

        self.message = switcher[error_code]
        self.error_code = error_code
        self.link = link


def get_json_dict(status):
    json_string = json.dumps(status._json)
    return json.loads(json_string)

# error message mentioned in MentionListener inside Function() def
def send_error_message(api, argument, child_status_json):
    try:
        api.send_direct_message(child_status_json["user"]["id"], f"The *{argument}* command you used is not valid.")
    except:
        logger.info(f"Could not send error message for some reason")
