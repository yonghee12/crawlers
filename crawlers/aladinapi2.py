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

headers = {'Connection': 'keep-alive', 'Accept': '*/*', 'Sec-Fetch-Dest': 'empty',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors',
                        'Referer': 'https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=247905989&start=main',
                        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9'}

isbn = 9791190030632
url = "https://www.aladin.co.kr/shop/product/getcontents.aspx?name=MyReview&Page=0&PageSize=1000&IsOrderer=2&ISBN="
url += str(isbn)
response = requests.get(url, headers=headers)
txt = response.text
bs = BeautifulSoup(txt, "lxml")
divs = bs.findAll('div', {'class': 'blog_list3'})
divs[0].findAll('a')
[a for a in bs.findAll('a') if a['href'].startswith("javascript:fn_toggle_mypaper")]


https://www.aladin.co.kr/ucl/shop/product/ajax/viewmypaperall.aspx?paperid=11979236&IsMore=1&communityType=MyReview

GET /ucl/shop/product/ajax/viewmypaperall.aspx HTTP/1.1
Accept: */*
Accept-Language: en-us
Host: www.aladin.co.kr
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15
Referer: https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=247906015
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
X-Requested-With: XMLHttpRequest

<a href="javascript:fn_toggle_mypaper(11979236,'MyReview')"><span class="Ere_str">이제 깨어날 시간이다. </span></a>


"""<a href="javascript:fn_toggle_mypaper(11952958,'MyPaper')"><span class="Ere_str">이러나저러나 내게는 마찬가지 </span></a>"""
https://www.aladin.co.kr/ucl/shop/product/ajax/viewmypaperall.aspx?paperid=11952958&IsMore=1&communityType=MyPaper
GET /ucl/shop/product/ajax/viewmypaperall.aspx HTTP/1.1
Accept: */*
Cookie: _ga=GA1.3.1217355330.1599719086; _gid=GA1.3.368600434.1599719086; ck_NotMylist=RowCount_detail=0&RowCount_simple=0&RowCount_short=0; _TRK_ASID_13987=05dc31c7c4028322cbe85ac020a0df00; _TRK_AUIDA_13987=9e69802d3d51e8fc2add4810771849e5:1; refererURL=https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=247906015; _BS_GUUID=tFUvR29arja4o2hXjA7rbWKbNmdxe2mIHhdzjnJK; ACEFCID=UID-5F59C6AD979444B24E683983; ACEUACS=1599719085641144627; AladdinSession=UID=-286049713&SID=THVX8y0xvfPs2sigtnCQ9w%3d%3d; AladdinUS=CAwLIJH0Xey4SvchAdtS1Q%3d%3d&USA=0; AladdinUser=UID=-286049713&SID=THVX8y0xvfPs2sigtnCQ9w%3d%3d
Accept-Language: en-us
Host: www.aladin.co.kr
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15
Referer: https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=247906015
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
X-Requested-With: XMLHttpRequest
