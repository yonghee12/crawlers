import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
sys.path = [str(PROJECT_ROOT)] + sys.path
print(PROJECT_ROOT)
print(sys.path)

import time

from slackutil.slack_util import *
from slackutil.slackconfig import *

slack = SlackClient(LOG_SLACK['API_TOKEN'], channel='nohup_log')
slack.send('send_logs init')


def watch(path):
    fp = open(path, 'r', encoding='utf8')
    while True:
        new = fp.readline()
        if new:
            yield new
        else:
            time.sleep(0.5)


filepath = '/home/ubuntu/logs/comments.out'
for newline in watch(filepath):
    slack.send(newline, force=True)
