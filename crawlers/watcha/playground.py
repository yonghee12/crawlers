import time
import random

import pandas as pd

from crawlers.watcha.functions import *
from header import get_headers_from_str, get_cookies_from_str
from header import WATCHA_EVAL_HEADERS, WATCHA_EVAL_COOKIES
from crawlers.watcha.functions import *
from crawlers.watcha.metadata_evaluations import WatchaMetadataHandler

keys = WatchaMetadataHandler.keys()
url = eval_links[keys[0]]
df = pd.DataFrame()
for i in range(0, 100):
    if i != 0 and i % 6 == 0:
        time.sleep(2)
    url = f'https://api-pedia.watcha.com/api/evaluations/movies?list_id=movies_{i}'
    res = get_api(url, headers=WATCHA_EVAL_HEADERS)
    result = res.get("metadata")
    if result and result.get('list'):
        df = df.append(pd.json_normalize(result))
        print(result)
    else:
        print(i, "not valid")
    time.sleep(0.05)

directory = os.path.join(ROOT_DIR, 'results')
if not os.path.exists(directory):
    os.mkdir(directory)
df.reset_index(inplace=True, drop=True)
filepath = os.path.join("results", f"categories_{len(df)}.csv")
path = os.path.join(ROOT_DIR, filepath)
df.to_csv(path)

print()

s = """movies_18	국내 누적관객수 TOP 영화
movies_19	역대 100만 관객 돌파 영화
movies_22	전세계 흥행 TOP 영화
movies_23	슈퍼 히어로
movies_24	스포츠 영화
movies_26	느와르
movies_27	저예산 독립 영화
movies_28	전문가 고평점 영화
movies_35	왓챠 평균별점 TOP 영화
movies_36	범죄
movies_37	드라마
movies_38	코미디
movies_39	로맨스/멜로
movies_40	스릴러
movies_41	로맨틱코미디
movies_42	전쟁
movies_44	가족
movies_45	판타지
movies_46	액션
movies_47	SF
movies_48	애니메이션
movies_49	다큐멘터리
movies_50	공포
movies_52	클래식"""

{v: k for k, v in [ss.split('\t') for ss in s.split('\n')]}