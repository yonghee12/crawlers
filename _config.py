import copy
import os
import sys
import re
import shutil as shutil
from datetime import datetime as dt, timedelta as timedelta
import pandas as pd
import pymysql as pm
import sqlalchemy as sa
import itertools
import sys
import redis
import slack as slackmodule
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import *
from progress_timer import Timer
from direct_redis import DirectRedis

# from .functions import bytes_to_float as bts

DGS = {'host': '192.168.100.122', 'user': 'alphabridge', 'password': 'asset1911!', 'port': 3306, 'charset': 'utf8'}

REDIS_TABLES = {
    "analysis_bella": 1,
    "nlp_wv": 2,
    "nlp_theme": 3,
    "notion": 4,
    "create_price": 11,
    "create_screening": 12,
    "create_backtesting": 13,
    "temp": 15
}

REDIS_INFO = {
    'dev': {
        "analysis_bella": {
            "host": '10.10.10.92', "port": 8020, "password": "algo1911", 'db': REDIS_TABLES['analysis_bella']},
        "nlp_wv": {
            "host": '10.10.10.92', "port": 8020, "password": "algo1911", 'db': REDIS_TABLES['nlp_wv']},
        "nlp_theme": {
            "host": '10.10.10.92', "port": 8020, "password": "algo1911", 'db': REDIS_TABLES['nlp_theme']},
        "create_price": {
            "host": '10.10.10.92', "port": 8020, "password": "algo1911", "db": REDIS_TABLES['create_price']},
        "create_screening": {
            "host": '10.10.10.92', "port": 8020, "password": "algo1911", "db": REDIS_TABLES['create_screening']},
        "create_backtesting": {
            "host": '10.10.10.92', "port": 8020, "password": "algo1911", "db": REDIS_TABLES['create_backtesting']},
        "notion": {
            "host": '10.10.10.92', "port": 8020, "password": "algo1911", 'db': REDIS_TABLES['notion']},

        "test_nlp_wv": {
            "host": '10.10.10.92', "port": 9020, "password": "algo1911", 'db': REDIS_TABLES['nlp_wv']},
        "test_nlp_theme": {
            "host": '10.10.10.92', "port": 9020, "password": "algo1911", 'db': REDIS_TABLES['nlp_theme']}
    },

    'depl': {
        "analysis_bella": {
            "host": '192.168.100.123', "port": 8020, "password": "algo1911", 'db': REDIS_TABLES['analysis_bella']},
        "nlp_wv": {
            "host": '192.168.100.123', "port": 8020, "password": "algo1911", 'db': REDIS_TABLES['nlp_wv']},
        "nlp_theme": {
            "host": '192.168.100.123', "port": 8020, "password": "algo1911", 'db': REDIS_TABLES['nlp_theme']},
        "create_price": {
            "host": '192.168.100.123', "port": 8020, "password": "algo1911", "db": REDIS_TABLES['create_price']},
        "create_screening": {
            "host": '192.168.100.123', "port": 8020, "password": "algo1911", "db": REDIS_TABLES['create_screening']},
        "create_backtesting": {
            "host": '192.168.100.123', "port": 8020, "password": "algo1911", "db": REDIS_TABLES['create_backtesting']},
    }
}

SLACK_AUTH_TOKEN = "xoxb-939769337249-999658780883-rKSFPjE96n5qzXaj9IOoYxXK"
SLACK_CHANNELS = {
    'slackbot_dev': 'C010D9ZGYH4',
    'slackbot_test': 'G011BQCP3QX',
    'test': 'G011BQCP3QX',
}

slack = slackmodule.WebClient(token=SLACK_AUTH_TOKEN)

NOTION_AUTH_TOKEN_V2 = "3d4448663441de52198cdd9569ea69effbabf5850ba77d1ac2025959d30d63f98d2eef8b73efed217bfb95fa76598719ccf00a1647e0b6cf25363438fe0d8c95a3b82da14ced596fb8af4eb15553"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))