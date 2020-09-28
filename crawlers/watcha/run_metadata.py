import pymysql as pm

from crawlers.watcha.api_handlers import WatchaMetadataHandler
from crawlers.watcha.config import *

stopwords = {'\"'}

def truncate():
    cur = conn.cursor()
    query = f"""
            TRUNCATE corpora.tb_watcha_metadata; 
            """.strip()
    print(query)
    cur.execute(query=query)
    conn.commit()


def update_metadata_using_api():
    for key in list(api.get_keys())[-3:]:
        print('-'*100 + '\n' + '-' * 100 + '\n' + f"{key}" + '\n' + '-'*100 + '\n' + '-' * 100)
        df = api.get(max_page=1000, category=key, verbose=1)
        df_db = df[['title', 'code', 'year', 'badges', 'ratings_avg', 'director_names', 'nations']]
        cur = conn.cursor()
        for idx, row in df_db.iterrows():
            title = row['title'].replace('\"', '')
            badges = ','.join([dic['name'] for dic in row['badges']])
            directors = ','.join(row['director_names'])
            nations = ','.join([dic['name'] for dic in row['nations']])
            query = f"""
                INSERT IGNORE INTO corpora.tb_watcha_metadata(title, code, year, badges, ratings_avg, director_names, nations) 
                VALUES("{title}", "{row['code']}", "{row['year']}", "{badges}", "{row['ratings_avg']}", "{directors}", "{nations}")
            """.strip()
            print(query)
            cur.execute(query=query)
            conn.commit()
        cur.close()


def main():
    if TRUNCATE:
        truncate()

    update_metadata_using_api()


if __name__ == "__main__":
    conn = pm.connect(**NIPA_DB_LOCAL)
    api = WatchaMetadataHandler(mod=6, default_wait=5.1, max_attempt=3)

    TRUNCATE = False
    main()
