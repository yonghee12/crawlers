import os
import sys
from pathlib import Path

ROOT = str(Path(__file__).parent.parent.parent.absolute())
sys.path = [ROOT] + sys.path

import time
import pickle
from typing import *
from importlib import reload
from time import perf_counter as now
from unicodedata import normalize

from urllib.parse import quote, unquote
import requests
from bs4 import BeautifulSoup, SoupStrainer
import pymysql as pm
import pandas as pd
from direct_redis import DirectRedis
from progress_timer import Timer

from _config import *
from crawlers.utils import get_safe
from functions import *


class NaverSearchMetadata:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
               'accept-language': 'ko;q=0.8,ko-KR;q=0.7'}

    def __init__(self, db_info, sql_verbose=0):
        self.db_info = db_info
        self.sql_verbose = sql_verbose
        self.conn = None
        self.connect()

    def connect(self):
        self.conn = pm.connect(**self.db_info)

    def convert_naver_date_to_mysql_date(self, timestr):
        return time.strftime('%Y-%m-%d', time.strptime(timestr, "%Y.%m.%d"))

    def get_links_and_insert(self, query, start_date, end_date, datestr, max_pages):
        page_idx = 0
        for step in range(0, max_pages + 1):
            index = step * 10 + 1

            print(f"{query}: {step}, {start_date} ~ {end_date}")
            url = f"https://search.naver.com/search.naver?&where=news&query={quote(query)}&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&ds={start_date}&de={end_date}&docid=&nso=so:r,p:from{datestr},a:all&mynews=0&cluster_rank=0&start={index}&refresh_start=0"

            page = get_safe(url, headers=self.headers)
            bs = BeautifulSoup(page, "lxml")

            page_inner = bs.find("div", {"class": "sc_page_inner"})
            page_prev = page_idx
            page_idx = page_inner.find("a", {'aria-pressed': 'true'}).get_text().strip()
            # print(f"page_prev: {page_prev}, current page: {page_idx}")
            if page_prev == page_idx:
                print(f"Query {query}, {datestr}는 {page_prev} 페이지가 마지막으로 판단되어 종료합니다.")
                return None

            atags = bs.findAll("a")
            news_links = [a.get('href') for a in atags if a.get_text() == "네이버뉴스" and a.get("href")]
            if not news_links:
                return None

            data = {
                'page': page_idx,
                'start_time': self.convert_naver_date_to_mysql_date(start_date),
                'end_date': self.convert_naver_date_to_mysql_date(end_date),
                'query': query,
                'links': news_links
            }

            print([a.get_text() for a in bs.findAll("a", {"class": "news_tit"})])

            self.insert_db_handler(data, verbose=self.sql_verbose)

    def insert_db_handler(self, data, verbose):
        try:
            self.insert_links(data, verbose)
        except Exception as e:
            print(str(e))
            self.connect()
            self.insert_links(data, verbose)

    def insert_links(self, data, verbose=0):
        cur = self.conn.cursor()
        search_query, typ, start_dt, end_dt, page = data['query'], "naver", data["start_time"], data['end_date'], data[
            'page']
        for link in data['links']:
            # noinspection SqlNoDataSourceInspection,SqlInsertValues
            query = f"""
            INSERT IGNORE INTO corpora.covid_crawl_metadata(
            SEARCH_QUERY, TYPE, START_DATE, END_DATE, LINK, PAGE, PARSED_YN
            ) 
            VALUES (
            "{search_query}", "{typ}", "{start_dt}", "{end_dt}", "{link}", "{page}", "0"
            );
            """.strip()
            if verbose > 0:
                print(query)
            cur.execute(query)
            self.conn.commit()
        cur.close()


if __name__ == "__main__":
    crawler = NaverSearchMetadata(db_info=NIPA_DB_LOCAL, sql_verbose=0)

    path = os.path.join(ROOT, "to_crawl.xlsx")
    queries = pd.read_excel(path, header=0, index_col=None)

    for idx, row in queries.iterrows():
        query, start_date, end_date = row['query'], row['start_date'], row['end_date']
        datestr = ''.join(start_date.split(".")) + 'to' + ''.join(end_date.split("."))
        crawler.get_links_and_insert(query, start_date, end_date, datestr, max_pages=100)

    print('hello')
    print()
