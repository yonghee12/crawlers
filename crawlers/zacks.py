import re
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

n_pages = 10
for symbol in ['AAPL', 'NFLX', 'IMMU', 'W', "LEVI"]:
    for page in range(1, n_pages + 1):
        url = f'https://www.zacks.com/stock/research/AAPL/all-news?page={page}&t={symbol}'
        print(url)
        req = Request(url, headers=headers)
        page = urlopen(req)
        bs = BeautifulSoup(page.read(), "lxml")
        items = bs.find_all('div', {'class': 'listitem'})

        titles, links = [], []
        for item in items:
            title = item.h1.text.strip()
            titles.append(title)
            links.append(item.a['href'])
            print(title)

        time.sleep(0.3)

        # try:
        #     profile_section = bs.find('section', {'class': re.compile("companyProfile.*")})
        #     profile_left = profile_section.find('section', {'class': re.compile("left.*")})
        #     desc = profile_left.get_text()
        #     print(symbol, desc)
        # except Exception as e:
        #     print(str(e))
        #     print("error:", symbol)

print()