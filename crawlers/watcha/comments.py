import time
import random

import pandas as pd

from watcha.functions import *

DEFAULT_WAIT = 5.1
wait = DEFAULT_WAIT

df = None
# content_id = 'mOVDyDz'  # 뮬란
# content_id = 'mWqJYmB'  # 닥터 두리틀
# content_id = 'mOo0pnP'  # 더넌
content_id = 'md76rgM'  # 스카이스크래퍼 1500+
order = 'popular'
n_min, n_max = get_n_comments(content_id)
print(f"n_max_commnets: {n_max}")

# TODO: def, class로 리팩토링해서 stop flag 없애기
stop = False
for i in range(1, n_max // 20 + 2):
    url = f'https://api-pedia.watcha.com/api/contents/{content_id}/comments?filter=all&order={order}&page={i}&size=20'
    result = get_watcha_reviews(url)
    if not result:
        if total >= n_max:
            stop = True
        else:
            attempt = 0
            while not result:
                print(i, "NO RESULTS")
                print(i, f'no results. waiting for {wait} sec.')
                time.sleep(wait)
                result = get_watcha_reviews(url)
                attempt += 1
                wait = DEFAULT_WAIT + attempt
                if total > n_min and attempt >= 3:
                    stop = True
                    break
            wait = DEFAULT_WAIT
    if stop:
        break
    df_local = pd.json_normalize(result)
    df = df.append(df_local) if df is not None else df_local
    total = len(df)
    print(i, df_local['user.name'].tolist())
    time.sleep(0.1 + random.random() / 2)
df.reset_index(inplace=True, drop=True)
df.to_csv(f'results/watcha_{content_id}_{order}_len{len(df)}.csv')

print()
