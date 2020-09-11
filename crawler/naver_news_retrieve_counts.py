import pandas as pd
from direct_redis import DirectRedis

from config_setting.config_redis import RedisConfig

RedisConfig.DEV_DEPL_choice = 'DEPL'
r = DirectRedis(**RedisConfig.REDIS_INFO.get('naver-news'))
exclude_poses = ['Punctuation', 'Number', 'Josa', 'Determiner', 'Suffix', 'Modifier']


def save_count_file(keyword):
    counts = r.hget('naver-news-counts', keyword)
    counts_filtered = [(item[0][0], item[0][1], item[1]) for item in counts if item[0][1] not in exclude_poses]
    df = pd.DataFrame(counts_filtered, columns=['word', 'pos', 'count'])
    print(df.head(1))
    df.to_excel(f'{keyword}.xlsx', header=True, index=False, encoding='cp949')


def main(saveall=False):
    if saveall:
        keywords = r.hkeys('naver-news-counts')
    else:
        keywords = ['우라늄']

    for keyword in keywords:
        save_count_file(keyword)


if __name__ == '__main__':
    main(saveall=False)