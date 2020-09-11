import re
from collections import Counter
from copy import deepcopy
from itertools import chain
from json import loads as jsondecoder
from unicodedata import normalize as nm
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from pprint import pprint

from bs4 import BeautifulSoup
from requests import get

from corpus.corpus.functions import get_tokenized_matrix, get_lemmatized_matrix
from zacks_news_retrieve_api import get_zacks_news_api_params

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


class ZacksCrawler:
    def __init__(self):
        self.token_errors = 0
        self.tokens = get_zacks_news_api_params()

    def rehash_tokens(self):
        self.tokens = get_zacks_news_api_params()

    def handle_zacks_api_result(self, query, step, start):
        result = get_zacks_api_result(query, step, start, tokens=deepcopy(self.tokens))
        if result != 'token error':
            return result
        else:
            if self.token_errors > 3:
                raise Exception("OVER API ERROR LIMIT")
            else:
                self.rehash_tokens()
                self.token_errors += 1
                return self.handle_zacks_api_result(query, step, start)

    def get_zacks_news_text_and_tokens(self, query, nums, step=20):
        urls_agg, texts_agg, tokens_agg = [], [], []
        for start in range(0, nums, step):
            data = self.handle_zacks_api_result(query, step, start)
            print(start, len(data))
            urls = [d.get('url') for d in data if d.get('url').split("//")[1].startswith("www.zacks.com/stock/news")]

            texts = get_zacks_bodies_from_urls(urls)
            tokens = get_tokenized_and_lemmatized_matrix(texts, flatten=True)

            urls_agg += urls
            texts_agg += texts
            tokens_agg += tokens

        counts = Counter(tokens_agg).most_common(200)
        return {'urls': urls_agg, 'texts': texts_agg, 'tokens': tokens_agg, 'counts': counts}


def make_zacks_url(query, step, start, params):
    params['num'] = [step]
    params['start'] = [start]
    del params['q']
    query_str = "&q=" + query + "%20more%3Astock_news"
    params_str = urlencode(params, doseq=True) + query_str
    url = "https://cse.google.com/cse/element/v1?" + params_str
    return url


def get_zacks_api_result(query, step, start, tokens=None):
    url = make_zacks_url(query, step, start, tokens)
    data = get(url).text
    startpos = re.search(".*api\d+\(", data).end()
    data = data[startpos:][:-2]
    if jsondecoder(data).get('error'):
        return 'token error'
    else:
        data = jsondecoder(data)['results']
    return data


def get_zacks_news_body(url):
    req = Request(url, headers=headers)
    page = urlopen(req)
    bs = BeautifulSoup(page.read(), "lxml")
    body = bs.find('div', {'id': 'comtext'})
    if body:
        text = body.get_text().strip()
        text = nm("NFKD", text)
        return text
    else:
        return None


def get_zacks_bodies_from_urls(urls):
    texts = []
    for idx, url in enumerate(urls):
        text = get_zacks_news_body(url)
        if text is not None:
            print(idx, text[:100])
            texts.append(text)
        else:
            print(idx, text, "returned None")
    return texts


def get_tokenized_and_lemmatized_matrix(texts, flatten=True):
    tokenized = get_tokenized_matrix(texts, tokenizer='word_tokenize', exclude_stopwords=True,
                                     stopwords_options=['punc', 'nltk'])
    lemmatized = get_lemmatized_matrix(tokenized)
    if flatten:
        return list(chain(*lemmatized))
    else:
        return lemmatized


zacks = ZacksCrawler()

def main():
    zacks_results = {}
    queries = ['apple']
    for query in queries:
        data = zacks.get_zacks_news_text_and_tokens(query, 20, step=20)
        zacks_results[query] = data
        return zacks_results
