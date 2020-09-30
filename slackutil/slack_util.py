import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
sys.path = [str(PROJECT_ROOT)] + sys.path
print(PROJECT_ROOT)
print(sys.path)

from slackutil.slackconfig import *
import os
from slack import WebClient
from slack.errors import SlackApiError


def send_slack(client, channel, message, force=False):
    assert isinstance(message, str)
    try:
        response = client.chat_postMessage(
            channel=channel, text=message)
        if not force:
            assert response["message"]["text"] == message
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")


class SlackClient:
    def __init__(self, token, channel):
        self._client = WebClient(token=token)
        self._channel = channel

    def send(self, message, force=False):
        send_slack(self._client, self._channel, message, force)

    def set_channel(self, channel):
        self._channel = channel


if __name__ == "__main__":
    slack = SlackClient(SLACK_API_TOKEN, channel='notionbot_test')
    slack.send('hello')
    print()