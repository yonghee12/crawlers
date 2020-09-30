import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
sys.path = [str(PROJECT_ROOT)] + sys.path
print(PROJECT_ROOT)
print(sys.path)

from time import sleep

import pymysql as pm
import pandas as pd

from crawlers.watcha.api_handlers import WatchaCommentsHandler
from crawlers.watcha.config import *


def truncate():
    cur = conn.cursor()
    query = "TRUNCATE tb_watcha_comments;"
    print(query)
    cur.execute(query=query)
    query = "UPDATE tb_watcha_metadata SET is_comments_parsed = 0"
    cur.execute(query=query)
    conn.commit()


def get_metadata_info():
    query = f"""
                SELECT title, code FROM corpora.tb_watcha_metadata
                WHERE is_comments_parsed=0 and no_comments=0
                ORDER BY id DESC;
    """.strip()
    print(query)
    return pd.read_sql(query, conn)


def print_info(index, titles, content_id):
    print(
        '-' * 100 + '\n' + '-' * 100 + '\n' + f"{index}/{len(titles)}: {titles[index]}, {content_id}" + '\n' + '-' * 100 + '\n' + '-' * 100)


def get_comments_main_query(row):
    text = row['text'].replace('\"', '').replace("\'", '').replace("\\", "")
    username = row['user.name'].replace('\"', '').replace("\'", '').replace("\\", "")
    query = f"""
                INSERT IGNORE INTO corpora.tb_watcha_comments(title, code, content_code, user_code, user_name, rating, text, 
                    watched_at, likes_count, replies_count, spoiler, improper, replyable, created_at) 
                SELECT m.title,
                    "{row['code']}", "{row['content_code']}", "{row['user_code']}", "{username}", 
                    "{row['user_content_action.rating']}", "{text}", "{row['watched_at']}", "{row['likes_count']}", 
                    "{row['replies_count']}", {row['spoiler']}, {row['improper']}, {row['replyable']}, 
                    "{row['created_at']}"
                FROM corpora.tb_watcha_metadata as m
                WHERE m.code="{row['content_code']}"
    """.strip()
    return query


def mark_is_comment_parsed_true(content_code):
    cur = conn.cursor()
    q = f"""UPDATE tb_watcha_metadata SET is_comments_parsed = 1 WHERE code="{content_code}";"""
    cur.execute(query=q)
    conn.commit()
    cur.close()


def mark_no_comment(content_code):
    cur = conn.cursor()
    q = f"""UPDATE tb_watcha_metadata SET no_comments = 1 WHERE code="{content_code}";"""
    cur.execute(query=q)
    conn.commit()
    cur.close()


def update_comments_using_api(idx, content_id, titles):
    index = START_FROM + idx
    print_info(index, titles, content_id)

    df = api.get(content_id, verbose=1, print_col='length')
    if df is None:
        print(f"There is no comment in {content_id}.")
        mark_no_comment(content_id)
        return False

    df_db = df[comments_columns]
    cur = conn.cursor()

    for row_idx, row in df_db.iterrows():
        query = get_comments_main_query(row)
        try:
            cur.execute(query=query)
            conn.commit()

        except Exception as e:
            print(str(e))
            print(f"ERROR on this query: {query}")
            print(f"{index}/{len(titles)}: {titles[index]}, {content_id}")
            return False

    print(row_idx, query)
    return True


def update_comments_using_api_handler(titles, content_ids):
    for idx, content_id in enumerate(content_ids):
        success = update_comments_using_api(idx, content_id, titles)
        if success:
            mark_is_comment_parsed_true(content_id)
        sleep(0.5)


def main():
    if TRUNCATE:
        truncate()

    metadata = get_metadata_info()
    metadata = metadata.iloc[START_FROM:, :]

    content_ids = list(metadata['code'])
    titles = list(metadata['title'])
    print(f"TOTAL CONTENT IDS: {len(content_ids)}")
    update_comments_using_api_handler(titles, content_ids)


def debug():
    # api.get("mdRL4eL")  # 기생충
    api.get("md76rgM")  # 스카이스크래퍼


if __name__ == "__main__":
    TRUNCATE = False
    START_FROM = 0
    MAX_ATTEMPT = 2

    conn = pm.connect(**NIPA_DB_LOCAL)
    api = WatchaCommentsHandler(mod=6, default_wait=5.1, max_attempt=MAX_ATTEMPT)
    stopwords = {'\"'}

    # debug()
    main()
