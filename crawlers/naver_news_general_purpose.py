import sys
from collections import Counter
from pprint import pprint
from itertools import chain

from direct_redis import DirectRedis

from config_setting.config_redis import RedisConfig
from corpus.corpus.naver_api import NaverNewsSearch
from corpus.corpus.tokenizers import KoreanTokenizer, get_nfc_text

tokenizer_name = 'mecab'
tok = KoreanTokenizer(tokenizer_name)
news_search = NaverNewsSearch()
print(tokenizer_name, tok)



def get_query_results(query, tokenize=False, max_len=1000):
    responses = news_search.get_news(query, max_len=max_len)
    newslist = []
    # texts_agg, tokens_agg = [], []
    for res in responses:
        if res['link'].startswith("https://news.naver.com"):
            try:
                body_text = news_search.get_naver_news_body(res['link'])
                body_text = get_nfc_text(body_text)
                if tokenize:
                    tokens = tok.pos(body_text)
                    res['tokens'] = tokens
                res['body'] = body_text
                newslist.append(res)
                # texts_agg.append(body_text)
                # tokens_agg += tokens
            except Exception as e:
                print(e)
    print(f"number of retrieved news: {len(newslist)}")
    # tokens_count = Counter(tokens_agg).most_common(1000)

    print(query)
    return newslist
    # pprint(tokens_count[:10])


def main():
    queries = ['현대중공업']
    for query in queries:
        res = get_query_results(query, 1000)


if __name__ == '__main__':
    # tokenizer_name = sys.argv[1] if sys.argv[1] else None
    main()