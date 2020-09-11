from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

for symbol in ['AAPL', 'NFLX', 'IMMU', 'W', "LEVI"][:1]:
    symbol = 'AAPL'
    url = f"https://www.nasdaq.com/market-activity/stocks/{symbol}"
    req = Request(url, headers=headers)
    page = urlopen(req)
    print(url)
    bs = BeautifulSoup(page.read(), "lxml")
    print()
    bs.find('div', {'class': 'company-profile'})
    print()
    try:
        desc = bs.find('div', {'class': 'tv-symbol-profile__description'}).get_text()
        print(symbol, desc)
    except Exception as e:
        print(str(e))
        print("error:", symbol)
