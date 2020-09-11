import time
import random

import pandas as pd

from crawlers.watcha.functions import *
from header import get_headers_from_str, get_cookies_from_str
from header import WATCHA_EVAL_HEADERS, WATCHA_EVAL_COOKIES

url = "https://api-pedia.watcha.com/api/evaluations/movies?list_id=movies_19"
s = """:method: GET
:scheme: https
:authority: api-pedia.watcha.com
:path: /api/evaluations/movies?list_id=movies_19
Accept: application/vnd.frograms+json;version=20
Accept-Language: en-us
Accept-Encoding: gzip, deflate, br
Host: api-pedia.watcha.com
Origin: https://pedia.watcha.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15
Referer: https://pedia.watcha.com/ko-KR/review
Connection: keep-alive
Cookie: _ga=GA1.1.1344425241.1599812825; _ga_1PYHGTCRYW=GS1.1.1599812825.1.1.1599812870.0; _guinness_session=jTlq8Olj%2BLjwPQ8v3PhQhbSBkhLHwplSwBUl3lpkIZPFQpnacGdj3vgllogTLu6SR8QPjjhFIfr4Fpw5v77tmtYwkszwu1kuB%2BkaFRFTygTe6GqqTrqSG23q2Asn--TOGUWcmL3rx8CZGo--NKDOU9YACb65I8Ljwvrg0Q%3D%3D; _gid=GA1.2.1662639084.1599812825; Watcha-Web-Client-Language=ko; _s_guit=53dbb556ea7893a49f5c44740df41c6f8af19413a0fd0931d84b8d4896ef; _gat=1
x-watcha-client-language: ko
x-watcha-client-version: 2.0.0
x-watcha-client: watcha-WebApp
x-watcha-client-region: KR
"""

c = """_ga=GA1.1.1344425241.1599812825; _ga_1PYHGTCRYW=GS1.1.1599812825.1.1.1599812870.0; _guinness_session=jTlq8Olj%2BLjwPQ8v3PhQhbSBkhLHwplSwBUl3lpkIZPFQpnacGdj3vgllogTLu6SR8QPjjhFIfr4Fpw5v77tmtYwkszwu1kuB%2BkaFRFTygTe6GqqTrqSG23q2Asn--TOGUWcmL3rx8CZGo--NKDOU9YACb65I8Ljwvrg0Q%3D%3D; _gid=GA1.2.1662639084.1599812825; Watcha-Web-Client-Language=ko; _s_guit=53dbb556ea7893a49f5c44740df41c6f8af19413a0fd0931d84b8d4896ef; _gat=1"""

headers = get_headers_from_str(s)
cookies = get_cookies_from_str(c)


