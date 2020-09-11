from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

for symbol in ['005930', '000020']:
    symbol = '000100'
    url = f"http://media.kisline.com/highlight/mainHighlight.nice?paper_stock={symbol}"
    req = Request(url, headers=headers)
    page = urlopen(req)
    bs = BeautifulSoup(page.read(), "lxml")
    try:
        desc_table = bs.find('table', {'class': 'list_a3', 'summary': '현황, 전망'})
        # 요기
        print()
        table = pd.read_html(str(desc_table))[0]
    except Exception as e:
        print(e)
        print("ERROR:", symbol)
        continue
