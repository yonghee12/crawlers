from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

for symbol in ['AAPL', 'NFLX', 'IMMU', 'W', "LEVI"]:

    url = f"https://finance.yahoo.com/quote/{symbol}/profile?p={symbol}"
    req = Request(url, headers=headers)
    page = urlopen(req)
    bs = BeautifulSoup(page.read(), "lxml")
    desc_section = bs.find('section', {'class': 'quote-sub-section Mt(30px)'})
    if desc_section.h2.get_text() == "Description":
        desc = desc_section.p.get_text()
        print(symbol)
        print(desc)
    else:
        print("error:", symbol, desc_section)
