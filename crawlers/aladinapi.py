import re
from bs4 import BeautifulSoup
import requests

ALADIN_HEADERS = {'Connection': 'keep-alive', 'Accept': '*/*', 'Sec-Fetch-Dest': 'empty',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                  'X-Requested-With': 'XMLHttpRequest', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors',
                  'Referer': 'https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=247905989&start=main',
                  'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9'}


def url_get(url, headers):
    response = requests.get(url, headers=headers)
    txt = response.text
    return BeautifulSoup(txt, "lxml")


def get_aladin_review_links(url: str, headers: dict):
    bs = url_get(url, headers)
    divs = bs.findAll('div', {'class': 'blog_list3'})
    link_head = "https://blog.aladin.co.kr"
    blog_links = []
    for div in divs:
        blog_links += [a['href'] for a in div.findAll('a') if a['href'].startswith(link_head) and not a.get('class')]
    return blog_links


def get_aladin_blog_body(url, headers):
    bs = url_get(url, headers)
    article = bs.find('div', {'class': 'article'})
    parphs = article.findAll("p")
    texts = ""
    for p in parphs:
        if p.script is not None:
            p.script.decompose()
        texts += '\n' + p.get_text(separator='\n').strip()
    texts = texts.replace('\xa0', ' ').replace('\u200b', '')
    texts = re.sub("[\n]+", "\n", texts)
    return texts.strip()


class AladinCrawl:
    def __init__(self):
        self.headers = ALADIN_HEADERS
        self.urls = {
            'myreview_bought': f"https://www.aladin.co.kr/shop/product/getContents.aspx?name=MyReview&Page=1&PageSize=1000&ISBN=",
            'myreview_all': f"https://www.aladin.co.kr/shop/product/getcontents.aspx?name=MyReview&Page=1&PageSize=1000&IsOrderer=2&ISBN=",
            'mypaper': f"https://www.aladin.co.kr/shop/product/getcontents.aspx?name=MyPaper&Page=1&PageSize=1000&ISBN="}

    def get_reviews(self, isbn, options):
        """
        options: 'myreview_bought', 'myreview_all', 'mypaper'
        """
        assert all([opt in self.urls for opt in options])
        isbn, h = str(isbn), self.headers
        links = []
        for opt in options:
            links += get_aladin_review_links(self.urls[opt] + isbn, h)
        return [get_aladin_blog_body(url, h) for url in links]


crawler = AladinCrawl()
reviews = crawler.get_reviews(9791157068166, ['myreview_all', 'mypaper'])
