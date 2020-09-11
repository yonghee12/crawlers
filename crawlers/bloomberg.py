import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

for symbol in ['AAPL', 'NFLX', 'IMMU', 'W', "LEVI"]:

    url = f"https://www.bloomberg.com/quote/{symbol}:US"
    req = Request(url, headers=headers)
    page = urlopen(req)
    bs = BeautifulSoup(page.read(), "lxml")
    try:
        profile_section = bs.find('section', {'class': re.compile("companyProfile.*")})
        profile_left = profile_section.find('section', {'class': re.compile("left.*")})
        desc = profile_left.get_text()
        print(symbol, desc)
    except Exception as e:
        print(str(e))
        print("error:", symbol)