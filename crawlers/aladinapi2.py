import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests



class AladinCrawl:
    def __init__(self):
        self.headers = {'Connection': 'keep-alive', 'Accept': '*/*', 'Sec-Fetch-Dest': 'empty',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors',
                        'Referer': 'https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=247905989&start=main',
                        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9'}
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

# headers = {'Connection': 'keep-alive', 'Accept': '*/*', 'Sec-Fetch-Dest': 'empty',
#                         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
#                         'X-Requested-With': 'XMLHttpRequest', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors',
#                         'Referer': 'https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=247905989&start=main',
#                         'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9'}
#
# isbn = 9791190030632
# url = "https://www.aladin.co.kr/shop/product/getcontents.aspx?name=MyReview&Page=0&PageSize=1000&IsOrderer=2&ISBN="
# url += str(isbn)
# response = requests.get(url, headers=headers)
# txt = response.text
# bs = BeautifulSoup(txt, "lxml")
# divs = bs.findAll('div', {'class': 'blog_list3'})
# divs[0].findAll('a')
# [a for a in bs.findAll('a') if a['href'].startswith("javascript:fn_toggle_mypaper")]