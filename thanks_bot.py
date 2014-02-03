import simplejson
import random
import requests
import re


# Bot settings
ACCESS_TOKEN = ""

# Set this to your full facebook name.
NAME = "Indradhanush Gupta"
BASE_URL = "https://graph.facebook.com"

# Time in seconds since epoch.
START_TIME = 1391193000
END_TIME = 1391279400


THANKYOU = [
    "Thanks!! :)",
    "Thank You!!  :)",
    "Thanks a lot!! :)",
    "Thanks a ton!! :)",
    "Thanks for your wishes!! :)"
]

regex = re.compile(".*h+a*p+i*y*e*(.*b([irthday]|['.]|(u*(d+(a+e+|a+y+|y+))))|(.*return(s|'s)))")


def get_wishes(START_TIME, END_TIME):
    payload = {
        "q" : "SELECT actor_id, post_id, message FROM stream WHERE source_id = me() AND created_time > %d AND created_time < %d limit 200;" % (START_TIME, END_TIME),
        "access_token" : ACCESS_TOKEN
    }
    url = "%s/fql" % (BASE_URL)
    response = requests.get(url, params=payload)
    data_set = simplejson.loads(response.text)["data"]
    print len(data_set)
    return data_set


def post_thanks(data_set):
    for data in data_set:
        wish = data["message"]
        if regex.match(wish):
            pass
        else:
            print "Regex match failed for message: %s" % (wish)
            override_regex = raw_input("Post thanks? (Y/N):")
            if override_regex == "y" or override_regex == "Y":
                pass
            else:
                continue
            
        post_id = data["post_id"]
        message = THANKYOU[random.randint(0, 4)]
        params = {"access_token": ACCESS_TOKEN}
        print wish, post_id
        comment_url = "%s/%s/comments" % (BASE_URL, post_id)        
        
        response = requests.get(comment_url, params=params)
        comments = simplejson.loads(response.text)["data"]
        reply_flag = False
        for comment in comments:
            if comment["from"]["name"] == NAME: #Already Commented.
                reply_flag = True
                break
        if reply_flag:
            print "Commented!"
            continue
        else:
            #Like the post.
            like_url = "%s/%s/likes" % (BASE_URL, post_id)
            params = {"access_token": ACCESS_TOKEN}
            response = requests.post(like_url, params=params)
            print response.text

            # Comment thanks on post.
            params["message"] = message
            response = requests.post(comment_url, data=params)
            print response.text


if __name__ == "__main__":
    data_set = get_wishes(START_TIME, END_TIME)
    post_thanks(data_set)

