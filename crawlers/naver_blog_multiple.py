from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from functools import reduce
from time import sleep

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

stopwords = {"\u200b", '\xa0'}

urls = [
    'https://blog.naver.com/PostView.nhn?blogId=zic6188610&logNo=221856333624', # 되는거
    "https://blog.naver.com/PostView.nhn?blogId=1004gofus&logNo=20209207240",   # 안되는거
    'https://blog.naver.com/PostView.nhn?blogId=goodnewslee&logNo=30069182378', # 안되는거
    'https://blog.naver.com/PostView.nhn?blogId=jesusclub77&logNo=221572046023' # 안되는거
]
for url in urls:
    req = Request(url, headers=headers)
    page = urlopen(req)
    soup = BeautifulSoup(page.read(), "lxml")
    if soup.find('div', {'id': 'postViewArea'}):
        postview = soup.find('div', {'id': 'postViewArea'})
        ptags = postview.find_all('p')
        # text = '\n'.join([p for ptag in ptags if (p := ptag.get_text().strip()) and p not in stopwords])
        text = '\n'.join([ptag.get_text().strip() for ptag in ptags if ptag.get_text().strip() and ptag.get_text().strip() not in stopwords])
        print(text)
    else:
        print('here')
        v = soup.find("div", {"class": "se-viewer"})
        v = soup.find_all("p", {"class": "se-text-paragraph"})

        tags = soup.find_all("span", {"class": "ell"})
        paragraphs = reduce(lambda x, y: x + "\n" + y.text, v, "")
        print(paragraphs)
    print('-' * 100)