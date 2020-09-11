# bs4
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

url = "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=105"
req = Request(url, headers=headers)
page = urlopen(req)
bs = BeautifulSoup(page.read(), "lxml")
print(str(bs)[:3000])

bs.contents