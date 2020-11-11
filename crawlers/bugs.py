import os

from utils import *
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from tqdm import tqdm


class BugsAlbumCrawler:
    def __init__(self, genre, genre_url):
        self.total_links = set()
        self.genre = genre
        self.genre_url = genre_url
        self.infos = {'기획사': set(),
                      '유통사': set()}

    def main(self, start_yymmdd):
        dt = datetime.strptime(start_yymmdd, '%Y%m%d')
        yymmdd = start_yymmdd
        while dt.year == 2020:
            links = self.get_album_links(yymmdd)
            self.get_infos(links)
            print(f"총 기획사 수 : {len(self.infos['기획사'])}, 총 유통사 수 : {len(self.infos['유통사'])}")
            self.write_file()
            dt = dt - timedelta(weeks=1)
            yymmdd = datetime.strftime(dt, "%Y%m%d")

    def get_album_links(self, yymmdd):
        url = f'https://music.bugs.co.kr/chart/track/week/{self.genre_url}?chartdate={yymmdd}'
        html = get_safe(url)
        bs = BeautifulSoup(html, 'lxml')

        chartweek = bs.find('div', {'id': 'CHARTweek'})
        atags = chartweek.find_all('a', {'class': 'album'})
        links = []
        for a in atags:
            link = a.get("href")
            if not link:
                continue
            link_small = link.split('?')[0]
            if link_small not in self.total_links:
                links.append(link)
                self.total_links.add(link_small)
        print(f"{yymmdd}, links: {len(links)}")
        return links

    def get_infos(self, links):
        for idx, link in enumerate(tqdm(links)):
            gi, yu = self.get_info(link)
            if gi is not None:
                self.infos['기획사'].add(gi)
            if yu is not None:
                self.infos['유통사'].add(yu)

    def write_file(self):
        with open(f'/Users/yonghee/Desktop/{self.genre}_기획사.txt', 'wb') as f:
            write = '\n'.join(sorted(self.infos['기획사'])).encode('utf8')
            f.write(write)

        with open(f'/Users/yonghee/Desktop/{self.genre}_유통사.txt', 'wb') as f:
            write = '\n'.join(sorted(self.infos['유통사'])).encode('utf8')
            f.write(write)

    @staticmethod
    def get_info_text(table, query):
        tag = table.find('th', string=query)
        if not tag:
            return None
        else:
            try:
                return tag.parent.td.text.strip()
            except:
                return None

    @staticmethod
    def get_info(album_link):
        try:
            html = get_safe(album_link)
            bs = BeautifulSoup(html, 'lxml')
            table = bs.find('table', {'class': 'info'}).tbody
            gi = BugsAlbumCrawler.get_info_text(table, '기획사')
            yu = BugsAlbumCrawler.get_info_text(table, '유통사')
            return gi, yu,
        except Exception as e:
            print(str(e))
            return None, None,


start_yymmdd = '20201102'
crawl_infos = [{'genre': '발라드', 'url': 'nb'},
               {'genre': '댄스_팝', 'url': 'ndp'},
               {'genre': '포크_어쿠스틱', 'url': 'nfa'},
               {'genre': '아이돌', 'url': 'nid'},
               {'genre': '랩_힙합', 'url': 'nrh'},
               {'genre': '알앤비_소울', 'url': 'nrs'},
               {'genre': '일렉트로닉', 'url': 'nkelec'},
               {'genre': '락_메탈', 'url': 'nkrock'}]

for info in crawl_infos:
    crawl = BugsAlbumCrawler(**info)
    crawl.main(start_yymmdd)
