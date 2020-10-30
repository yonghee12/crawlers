# -*- coding: utf8 -*-

import os

os.putenv("PYTHONIOENCODING", "UTF-8")
os.system("export PYTHONIOENCODING=UTF-8")

import sys
from pathlib import Path

ROOT = str(Path(__file__).parent.parent.parent.absolute())
sys.path = [ROOT] + sys.path

import re
import json
import time
import pickle
from typing import *
from pprint import pprint
from importlib import reload
from time import perf_counter as now
from unicodedata import normalize

from urllib.parse import quote, unquote, urlencode, parse_qs, parse_qsl
import requests
from bs4 import BeautifulSoup, SoupStrainer
import pymysql as pm
import pandas as pd
from direct_redis import DirectRedis
from progress_timer import Timer

from _config import *
from crawlers.utils import get_safe
from functions import *

decoder = json.decoder.JSONDecoder()

headers = {'authority': 'apis.naver.com',
           'method': 'GET',
           # 'path': '/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=view_life&pool=cbox5&_callback=jQuery112408625504614686463_1603957406104&lang=ko&country=KR&objectId=news277%2C0004757910&categoryId=&pageSize=10&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=1&initialize=true&userType=&useAltSort=true&replyPageSize=20&sort=favorite&includeAllStatus=true&_=1603957406106',
           'scheme': 'https',
           'accept': '*/*',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'en-US,en;q=0.9',
           'referer': 'https://news.naver.com/',
           'sec-ch-ua': '"Chromium";v="86", ""Not\\A;Brand";v="99", "Google Chrome";v="86"',
           'sec-ch-ua-mobile': '?0',
           'sec-fetch-dest': 'script',
           'sec-fetch-mode': 'no-cors',
           'sec-fetch-site': 'same-site',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

naver_comments_api_head = "https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_life&pool=cbox5&lang=ko&country=KR&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&initialize=true&userType=&useAltSort=true&replyPageSize=20&sort=favorite&includeAllStatus=true"
conn = pm.connect(**NIPA_DB_LOCAL)


def get_metadata_info(conn, source, limit=None):
    assert source in ['naver', 'nate']
    query = f"""-- noinspection SqlNoDataSourceInspectionForFile
                SELECT * FROM corpora.covid_crawl_metadata
                WHERE PARSED_YN=0 AND TYPE="{source}"
                ORDER BY IDX ASC;
    """.strip()
    if limit is not None and isinstance(limit, int):
        query = query[:-1] + f" LIMIT {limit};"
    print(query)
    return pd.read_sql(query, conn)


def insert_links(data, conn, verbose=0):
    cur = conn.cursor()
    search_query, source, news_link = data['metainfo']
    for comment_id, reg_dt, comment in data['commentinfo']:
        comment_escaped = comment.replace('\"', '').replace("\'", '').replace("\\", "")
        query = f"""-- noinspection SqlNoDataSourceInspectionForFile
        INSERT IGNORE INTO corpora.covid_crawl_comment(
        COMMENT_ID, SEARCH_QUERY, TYPE, NEWS_LINK, REG_DT, COMMENT
        ) 
        VALUES (
        "{comment_id}", "{search_query}", "{source}", "{news_link}", "{reg_dt}", "{comment_escaped}"
        );
        """.strip()
        if verbose > 0:
            print(query)
        cur.execute(query)
        conn.commit()
    cur.close()


def mark_parsed_yn_true(link):
    cur = conn.cursor()
    q = f"""UPDATE corpora.covid_crawl_metadata SET PARSED_YN = 1 WHERE LINK="{link}";"""
    cur.execute(query=q)
    conn.commit()
    cur.close()


def get_and_insert_comments_from_naver_news(news_link, search_query, max_pages):
    news_queries = dict(parse_qsl(news_link))
    oid, aid = news_queries.get('oid'), news_queries.get('aid')
    if oid is None or aid is None:
        return None
    object_id = quote(f"news{oid},{aid}")

    for page in range(1, max_pages + 1):
        url = naver_comments_api_head + f"&page={page}&objectId={object_id}"
        html = get_safe(url, headers=headers)
        try:
            if html.startswith('jQuery'):
                html = re.sub("jQuery.+\(", '', html)
            elif html.startswith("_callback"):
                html = re.sub("_callback\(", '', html)
            else:
                raise Exception(f"html starts with {html[:100]}")
            html = re.sub("\);$", '', html)
            result = decoder.decode(html)
            comment_list = result['result']['commentList']
            comments = []
            for row in comment_list:
                cid = row['objectId'].replace(',', '-') + '-' + str(row['commentNo'])
                reg_dt = row['regTime'].split("T")[0]
                comment = row['contents']
                # comment = comment.encode("utf8")
                if comment:
                    # print(reg_dt, comment)
                    comments.append((cid, reg_dt, comment,))

            if not comments:
                break

            data = {'metainfo': (search_query, 'naver', news_link,),
                    'commentinfo': comments}

            insert_links(data, conn, verbose=0)

            if page == 1:
                dt = sorted([r[1] for r in comments])[0]
                print(f"{search_query}, {dt}, {news_link}")
                print("samples:", [r[2] for r in comments][:3])

        except Exception as e:
            print(f"오류 발생한 뉴스링크 : {news_link}, api 링크 : {url}")
            print(str(e))


def main(metadata):
    for idx, row in metadata.iterrows():
        get_and_insert_comments_from_naver_news(row['LINK'], row['SEARCH_QUERY'], max_pages=20)
        mark_parsed_yn_true(row['LINK'])


if __name__ == '__main__':
    while True:
        metadata = get_metadata_info(conn, source='naver')
        if metadata.empty:
            time.sleep(10)
            metadata = get_metadata_info(conn, source='naver')
            if metadata.empty:
                break
        main(metadata)
