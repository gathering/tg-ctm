from django.contrib.auth.models import User
from django.conf import settings
import requests
from urllib.parse import quote

# slack utils
def send_message_to_user(user, message):
    user_email = user.username
    slack_user = slack_request("get", "users.lookupByEmail?email=" + user_email).json()
    if not slack_user['ok']: return False

    slack_user_id = slack_user['user']['id']
    slack_message = slack_request("post", "chat.postMessage?channel=" + slack_user_id + "&text=" + quote(message)).json()
    if not slack_message['ok']: return False

    return True

def slack_request(method, path):
    headers = { "Authorization": "Bearer " + settings.SLACK_CLIENT_TOKEN }
    return requests.request(method, "https://slack.com/api/" + path, headers=headers)
