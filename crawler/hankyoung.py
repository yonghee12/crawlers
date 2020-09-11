from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from requests import get
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

url = "http://consensus.hankyung.com/apps.analysis/analysis.downpdf?report_idx=557012"
req = Request(url, headers=headers)
page = urlopen(req)
bs = BeautifulSoup(page.read(), "lxml")

print()