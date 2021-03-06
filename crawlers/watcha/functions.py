import os
import time
import random

from pathlib import Path

PROJECT_ROOT = Path().parent.parent.absolute()

from importlib import reload
from string import digits
from urllib.parse import quote
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import pandas as pd

from rootconfig import ROOT_DIR
from header import WATCHA_HEADERS as watcha_default_headers
from header import WATCHA_EVAL_HEADERS, WATCHA_EVAL_COOKIES
from crawlers.watcha.config import *

digits = set(digits)


def get_api(url, error=0, **kwargs):
    options = {}
    if kwargs.get('headers'):
        options.update({'headers': kwargs['headers']})
    elif kwargs.get('cookies'):
        options.update({'headers': kwargs['headers']})

    try:
        if options:
            response = requests.get(url, **options)
        else:
            response = requests.get(url, headers=watcha_default_headers)
    except Exception as e:
        if error > 2:
            return dict()
        print(str(e), 'RELOADING REQUESTS MODULE')
        reload(requests)
        time.sleep(5.1)
        return get_api(url, error + 1, **kwargs)
    else:
        if response.status_code == 200:
            try:
                result = response.json()
                return result
            except:
                return dict()
        else:
            return dict()


def get_html(url):
    response = requests.get(url, headers=watcha_default_headers)
    bs = BeautifulSoup(response.text, "lxml")
    return bs


def search_results(query):
    query = quote(query)
    url = f'https://api-pedia.watcha.com/api/searches?query={query}'
    res = get_api(url)
    result = res['result']['top_results']
    return result


def get_watcha_reviews(url):
    res = get_api(url)
    result = res.get('result')
    if result:
        result = result.get('result')
    return result


def get_api_result(url):
    res = get_api(url, headers=WATCHA_EVAL_HEADERS, cookies=WATCHA_EVAL_COOKIES)
    result = res.get('result')
    result = result.get('result') if result else None
    return result


def get_n_comments(content_id):
    url = f'https://pedia.watcha.com/ko-KR/contents/{content_id}'
    try:
        bs = get_html(url)
        n_comments = bs_n_comments(bs)
        return n_comments
    except Exception as e:
        print(str(e))
        return 0, 0,


def bs_n_comments(bs):
    comment_header = [h for h in bs.find_all('header') if h.h2.text == '코멘트']
    if not comment_header:
        return 0, 0,
    comment_header = comment_header[0]
    text = comment_header.find('span').text
    n_comments = ''
    for l in text:
        if l in digits:
            n_comments += l
    power = len(n_comments)
    n_comments = int(n_comments)
    min_comments = int(n_comments * 0.9)
    max_comments = n_comments + (10 ** (power - 1))
    return min_comments, max_comments
