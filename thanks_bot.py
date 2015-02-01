"""
Birthday thanks bot.
"""

# System imports
import sys
import random
import re

# Third party imports
import simplejson
import requests

# Local imports
import settings

regex = re.compile(".*h+a*p+i*y*e*(.*b([irthday]|['.]|(u*(d+(a+e+|a+y+|y+))))|(.*return(s|'s)))")


def get_wishes(start_time, end_time):
    """
    Fetches facebook wall posts between a given time range.

    :param start_time: Lower range of seconds since epoch.
    :type start_time: int
    :param _time: Upper range of seconds since epoch.
    :type _time: int

    :return: List of posts
    :type: list
    """
    sys.stdout.write('Fetching your wishes...')
    sys.stdout.flush()
    payload = {
        "q" : "SELECT actor_id, post_id, message FROM stream WHERE source_id = me() AND created_time > %d AND created_time < %d limit 200;" % (start_time, end_time),
        "access_token" : settings.ACCESS_TOKEN
    }
    url = "%s/fql" % (settings.BASE_URL)
    response = requests.get(url, params=payload)
    data_set = simplejson.loads(response.text)["data"]
    sys.stdout.write('OK\n')
    sys.stdout.flush()

    return data_set


def post_thanks(data_set, match_regex=True):
    """
    Likes and comments on posts.

    :param data_set: List of facebook posts.
    :type data_set: list
    :param match_regex: Indicate whether post message is to be matched
                        with regex or not.
    :type match_regex: bool

    :return: List of posts that failed regex match.
    :type: list
    """
    failed_matches = []

    sys.stdout.write('Posting...')
    sys.stdout.flush()
    for data in data_set:
        wish = data["message"].lower().strip()
        if match_regex and regex.match(wish) is None:
            failed_matches.append(data)
        else:
            post_id = data["post_id"]
            message = settings.REPLIES[random.randint(0, 4)]
            params = {
                "access_token": settings.ACCESS_TOKEN
            }
            comment_url = "%s/%s/comments" % (settings.BASE_URL, post_id)

            response = requests.get(comment_url, params=params)
            comments = simplejson.loads(response.text)["data"]
            already_replied = False

            for comment in comments:
                if comment["from"]["name"] == settings.NAME: # Already Commented.
                    already_replied = True
                    break

            if not already_replied:
                #Like the post.
                like_url = "%s/%s/likes" % (settings.BASE_URL, post_id)
                response = requests.post(like_url, data=params)
                sys.stdout.write('.')
                sys.stdout.flush()

                # Comment thanks on post.
                params["message"] = message
                response = requests.post(comment_url, data=params)
                sys.stdout.write('.')
                sys.stdout.flush()

    sys.stdout.write('OK\n')

    return failed_matches


if __name__ == "__main__":
    data_set = get_wishes(settings.START_TIME, settings.END_TIME)
    failed_matches = post_thanks(data_set)
    if failed_matches:
        check_failed_matches = raw_input(
            'Regex failed for some posts. Wanna check? (Y/N):')

        if check_failed_matches.lower().strip() == 'y':
            force_post = []
            for msg in failed_matches:
                print 'Failed message: {msg}'.format(msg=msg['message'])
                override_regex = raw_input('Post thanks? (Y/N):')
                if override_regex.lower().strip() == 'y':
                    force_post.append(msg)

            if force_post:
                post_thanks(force_post, match_regex=False)
