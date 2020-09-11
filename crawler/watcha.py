# bs4
import time
import random
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests

import pandas as pd

from header import WATCHA_HEADERS as headers

def get_watcha_reviews(url):
    response = requests.get(url, headers=headers)
    res = response.json()
    result = res['result']['result']
    return result

df = None
content_id = 'mdRL4eL'
order = 'popular'
for i in range(1, 10):
    url = f'https://api-pedia.watcha.com/api/contents/{content_id}/comments?filter=all&order={order}&page={i}&size=20'
    # url = f'https://api-pedia.watcha.com/api/contents/{content_id}/comments?filter=all&order={order}&page=43&size=3'
    # response = requests.get(url, headers=headers, cookies=cookies)
    result = get_watcha_reviews(url)
    if not result:
        print(i, "NO RESULTS")

    df_local = pd.json_normalize(result)
    df = df.append(df_local) if df is not None else df_local
    print(df_local['user.name'].tolist())
    time.sleep(0.3 + random.random()/2)
df.reset_index(inplace=True, drop=True)
df.to_csv(f'results/watcha_{content_id}_{order}_len{len(df)}.csv')

print()