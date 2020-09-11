# TODO: lists:25의 의미, 몇개 가져올 것인지 파악
# TODO: 보편적인 api handler 만들기


from crawlers.watcha.functions import *

category = '역대 100만 관객 돌파 영화'
URL_HEAD = eval_links[category]

DEFAULT_WAIT = 5.1
wait = DEFAULT_WAIT

df = None
# TODO: def, class로 리팩토링해서 stop flag 없애기
stop = False
total = 0
for i in range(1, 100):
    if i != 1 and i % 6 == 1:
        time.sleep(6.1)
    url = URL_HEAD + f"&page={i}&size=20"
    result = get_eval_result(url)
    if not result:
        attempt = 0
        while not result:
            print(i, f'no results. waiting for {wait} sec.')
            time.sleep(wait)
            result = get_eval_result(url)
            attempt += 1
            wait = DEFAULT_WAIT + attempt
            if attempt >= 4:
                stop = True
                break
            wait = DEFAULT_WAIT
    if stop:
        break
    df_local = pd.json_normalize(result)
    df = df.append(df_local) if df is not None else df_local
    total = len(df)
    print(i, [r.get('title') for r in result])
    time.sleep(0.1 + random.random() / 2)
df.reset_index(inplace=True, drop=True)
filepath = os.path.join("results", f'watcha_eval_{category}_len{len(df)}.csv')
path = os.path.join(ROOT_DIR, filepath)
df.to_csv(path)

print()

