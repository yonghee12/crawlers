import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests

from header import ALADIN_HEADERS


def get_aladin_review_links(url: str, headers: dict):
    response = requests.get(url, headers=headers)
    txt = response.text
    bs = BeautifulSoup(txt, "lxml")
    divs = bs.findAll('div', {'class': 'blog_list3'})
    link_head = "https://blog.aladin.co.kr"
    blog_links = []
    for div in divs:
        blog_links += [a['href'] for a in div.findAll('a') if a['href'].startswith(link_head) and not a.get('class')]
    return blog_links


def get_aladin_blog_body(url, headers):
    req = Request(url, headers=headers)
    page = urlopen(req)
    bs = BeautifulSoup(page.read(), "lxml")
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
reviews = crawler.get_reviews(9791190030632, ['myreview_all', 'mypaper'])

with open('temp.txt', 'w') as f:
    f.write('\n\n'.join(reviews))

