from config import *
import os
from slack import WebClient
from slack.errors import SlackApiError


def send_slack(client, channel, message):
    assert isinstance(message, str)
    try:
        response = client.chat_postMessage(
            channel=channel, text=message)
        assert response["message"]["text"] == message
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")


class SlackClient:
    def __init__(self, token, channel):
        self._client = WebClient(token=token)
        self._channel = channel

    def send(self, message):
        send_slack(self._client, self._channel, message)

    def set_channel(self, channel):
        self._channel = channel
