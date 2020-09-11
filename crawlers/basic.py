# bs4
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

url = "https://news.naver.com/"
req = Request(url, headers=headers)
page = urlopen(req)
bs = BeautifulSoup(page.read(), "lxml")
print(bs.findAll("div", {"class": "hdline_article_tit"}))

# login
import requests

url = 'https://job.sogang.ac.kr/ajax/common/loginproc2.aspx'
session = requests.Session()
per_session = session.post(url, data={'userid': '20121177', 'passwd': 'cjsdydgml2@'})
soup = BeautifulSoup.BeautifulSoup(session.get(url).content)
