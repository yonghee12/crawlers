from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from unicodedata import normalize as nm

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


def get_naver_news_body(link, errors=0):
    if errors > 3:
        print('error limit exceeded')
        return None

    url = link
    req = Request(url, headers=headers)
    try:
        page = urlopen(req)
        bs = BeautifulSoup(page.read(), "lxml")
        body = bs.find('div', {'id': 'articleBodyContents'})
        for script in body.select('script'):
            script.extract()
        text = body.get_text().strip()
        text = nm("NFKD", text)
        return text
    except Exception as e:
        if "urllib.error.HTTPError: HTTP Error 504: Gateway Time-out" in str(e):
            errors += 1
            get_naver_news_body(link, errors)
        else:
            raise e
