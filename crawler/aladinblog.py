# bs4
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from unicodedata import normalize

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

url = "https://blog.aladin.co.kr/778144108/9240678"
req = Request(url, headers=headers)
page = urlopen(req)
bs = BeautifulSoup(page.read(), "lxml")
article = bs.find('div', {'class': 'article'})
paragraphs = article.findAll("p")
text = '\n'.join([p.get_text('\n') for p in paragraphs if p.text and (not p.text.strip().startswith("var js"))]).strip()
text = text.replace('\xa0', ' ')
text = re.sub("[\n]+", "\n", text)
text
print()