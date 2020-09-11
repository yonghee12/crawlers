from _config import *
from corpus.corpus import SimpleCorpus
from corpus.corpus.search_tokens import *
from corpus.corpus.presets import stopwords_compiliation as eng_stopwords


def get_keypair():
    conn = pm.connect(**DGS)
    sql = "SELECT * FROM dg_db_refine_mgt.tb_security_master_new;"
    dt_pair = pd.read_sql(sql, conn)
    conn.close()
    dt_pair = dt_pair[['SYMBOL', 'REP_NO', 'CMP_NM_ENG']]
    return dt_pair


def get_dart():
    conn = pm.connect(**DGS)
    sql = "SELECT * FROM dg_db_crawl.tb_nlp_dart_contents;"
    df = pd.read_sql(sql, conn)
    conn.close()
    return df


def get_kisline():
    conn = pm.connect(**DGS)
    sql = "SELECT RIC, MAIN_PRODUCTS, SUBSTR(SUMMARY,6) SUMMARY FROM dg_db_crawl.tb_kisline_cmp_info;"
    df = pd.read_sql(sql, conn)
    conn.close()
    return df


def get_naver_finance():
    conn = pm.connect(**DGS)
    sql = "SELECT RIC, SUMMARY FROM dg_db_crawl.tb_naver_company_summary;"
    df = pd.read_sql(sql, conn)
    conn.close()
    return df


def get_dart_contracts():
    conn = pm.connect(**DGS)
    sql = "SELECT SYMBOL, CATEGORY, CONTRACT_NM FROM dg_db_crawl.tb_nlp_dart_contract_nm;"
    df = pd.read_sql(sql, conn)
    conn.close()
    return df


def get_korean_biz_stopwords(filepath):
    freqs = pd.read_excel(filepath, header=0, index_col=None)
    stopwords = freqs.word[freqs.use_bool.isna()].to_list()
    return stopwords


def get_tokenized_matrix_korean(texts, tokenizer, include_all_poses=False, exclude_stopwords=True):
    tokenized = []
    timer = Timer(len(texts))
    for idx, text in enumerate(texts):
        timer.time_check(idx)
        try:
            posed = tokenizer.pos(text)
            posed_includes = [t[0] for t in posed if
                              (include_all_poses or (not include_all_poses and t[1] in tokenizer.include_poses))
                              and (not exclude_stopwords or not is_stopwords(t[0]))]
            tokenized.append(posed_includes)
        except Exception as e:
            print(str(e))
    return tokenized


def expand_bigram(lemmatized_matrix):
    for lemm in lemmatized_matrix:
        lemm.extend([''.join([lemm[i], lemm[i + 1]]) for i in range(len(lemm) - 1) if lemm[i] != lemm[i + 1]])
    return lemmatized_matrix


def get_keywords_df(corp: SimpleCorpus, tokenizer='mecab', top=30, metric='freq', return_type='df', savefile=False,
                    filepath=None, bigram=False):
    tok = KoreanTokenizer(tokenizer)
    if metric in ['freq', 'frequency']:
        corp.lemmatized_matrix = get_tokenized_matrix_korean(corp.texts, tok, include_all_poses=True,
                                                             exclude_stopwords=True)
        corp.lemmatized_matrix = expand_bigram(corp.lemmatized_matrix) if bigram else corp.lemmatized_matrix
        if return_type == 'counter':
            corp.counted_matrix = [Counter(lemm) for lemm in corp.lemmatized_matrix]
            return corp.counted_matrix
        elif return_type == 'df':
            corp.counted_matrix = [sorted(Counter(lemm).items(), key=lambda x: x[1], reverse=True)[:top] for lemm in
                                   corp.lemmatized_matrix]
            top_words = [', '.join([t[0] for t in lemm]) for lemm in corp.counted_matrix]
            return pd.DataFrame(data={
                'REP_NO': corp.repnos,
                'COMPANY': corp.names,
                'TOP_WORDS': top_words
            })
    elif metric in ['tfidf', 'tf-idf']:
        corp.lemmatized_matrix = get_tokenized_matrix_korean(corp.texts, tok, include_all_poses=False)
        corp.make_tfidf_scores_series_matrix(number_of_tops=top)
        tfidf = corp.get_tfidf_top_words_df(number_of_tops=top)
        tfidf = tfidf.drop(['EMPLOYEES', 'COUNTRY'], axis=1)
    else:
        raise Exception('Metric Error')

    if savefile:
        filepath = filepath if filepath else f'tokenized/dart_tfidf_{tokenizer}_top{top}.xlsx'
        tfidf.to_excel(filepath, index=False, header=True, encoding='cp949')


def freq_all(corp: SimpleCorpus, tok: KoreanTokenizer, filepath, top=10000, minimum=10):
    texts = corp.texts
    big_counter = Counter()
    timer = Timer(len(texts))
    for idx, text in enumerate(texts):
        timer.time_check(idx)
        posed = tok.pos(text)
        # posed = [t for t in posed if t[1] in tokenizer.include_poses and not biz_stopwords_hash.get(t[0])]
        posed = [t for t in posed if t[1] in tok.include_poses]
        big_counter.update(Counter(posed))

    counts = big_counter.most_common(top)
    # counts_filt = [(item[0][0], item[0][1], item[1]) for item in counts if item[0][1] in include_poses and item[1] > 30]
    counts_filt = [(item[0][0], item[0][1], item[1]) for item in counts if item[1] > minimum]
    result_df = pd.DataFrame(counts_filt, columns=['word', 'pos', 'count'])
    result_df.to_excel(filepath, header=True, index=False, encoding='cp949')


def make_index_file(corpus, tokenizer, filepath):
    counters = []
    timer = Timer(len(corpus.texts))
    for idx, tup in enumerate(zip(corpus.repnos, corpus.texts)):
        repno, text = tup
        try:
            timer.time_check(idx)
            posed = tokenizer.pos(text)
            posed_includes = [t for t in posed if t[1] in tok.include_poses and not biz_stopwords_hash.get(t[0])]
            counters.append(Counter(posed_includes).most_common(30))
        except Exception as e:
            print(str(e))
    # counts_unpacked = [[(item[0][0], item[0][1], item[1]) for item in counts] for counts in counters]
    counts_words = [[item[0][0] for item in counts] for counts in counters]
    counts_words_joined = [','.join(arr) for arr in counts_words]
    result_df = pd.DataFrame(data={
        'repno': corpus.repnos,
        'name': corpus.names,
        'words': counts_words_joined
    })
    result_df.to_excel(filepath, header=True, index=False, encoding='utf-8')
    return result_df


def reverse_index(corp):
    app = SearchTokensIndexing(tokenizer='mecab')
    docs = {
        'keys': ['name', 'contents'],
        'data': [{'name': name, 'contents': content} for name, content in zip(corp.names, corp.texts) if content]
    }
    app.make_index(docs, primary='name', exclude=['name'])
    # app.indexed_docs
    app.search('완성차')

    # make_index_file(corp, tokenizer)


def get_regex_tokenized(corpus, savefile=False, filepath=None):
    counters = []
    for text in corpus.texts:
        tokens = re_nonum_nohyphen.findall(text)
        ct = Counter(tokens).most_common(30)
        counters.append(ct)
    counts_words_joined = [', '.join([item[0] for item in counts]) for counts in counters]
    result_df = pd.DataFrame(data={
        'repno': corpus.repnos,
        'name': corpus.names,
        'words': counts_words_joined
    })
    if savefile:
        filepath = filepath if filepath else 'tokenized/keywords_regex_tokenized.xlsx'
        result_df.to_excel(filepath, header=True, index=False, encoding='utf-8')
    return result_df


def get_processed_kisline():
    kisline = get_kisline()
    kisline = kisline[['RIC', 'SUMMARY']]
    kisline['REP_NO'] = kisline['RIC'].apply(lambda x: keypair_ko_repno.get(x))
    kisline['NAME'] = kisline['REP_NO'].apply(lambda x: keypair_names.get(x))
    kisline = kisline.dropna(inplace=False)
    kisline = kisline.drop('RIC', axis=1, inplace=False)
    kisline = kisline.rename(columns={"SUMMARY": "KISLINE_SUMMARY"}, inplace=False)
    return kisline


def get_processed_nf():
    nf = get_naver_finance()
    nf['REP_NO'] = nf['RIC'].apply(lambda x: keypair_ko_repno.get(x))
    nf['NAME'] = nf['REP_NO'].apply(lambda x: keypair_names.get(x))
    nf = nf.dropna(inplace=False)
    nf = nf.drop('RIC', axis=1, inplace=False)
    nf = nf.rename(columns={"SUMMARY": "NAVER_SUMMARY"}, inplace=False)
    return nf


def kisline_nf_main():
    kl = get_processed_kisline()
    nf = get_processed_nf()
    merged = pd.merge(left=kl, right=nf, how='inner', on=['REP_NO', 'NAME'])
    merged['SUMMARY_CONCAT'] = merged['NAVER_SUMMARY'] + '\n' + merged['KISLINE_SUMMARY']
    concat_df = merged[['REP_NO', 'NAME', 'SUMMARY_CONCAT']]
    corp = SimpleCorpus(concat_df, repno_col='REP_NO', text_col='SUMMARY_CONCAT', name_col='NAME')
    make_index_file(corp, tok, 'tokenized/kisline_and_nf_freq_with_stopwords.xlsx')
    freq_all(corp, tok, filepath='tokenized/kisline_and_nf_freq_all.xlsx', top=10000)


def get_processed_dartcon():
    dartcon = get_dart_contracts()
    dartcon['REP_NO'] = dartcon['SYMBOL'].apply(lambda x: keypair_ko_repno.get(x))
    dartcon['NAME'] = dartcon['REP_NO'].apply(lambda x: keypair_names.get(x))
    dartcon = dartcon[['REP_NO', 'NAME', 'CONTRACT_NM']]
    dartcon = dartcon.dropna(inplace=False)
    return dartcon


def dartcon_main():
    df = get_processed_dartcon()
    df['CONTRACT_NM'].apply(lambda x: x.split(' '))
    for s in df['CONTRACT_NM'][10:100]:
        print(s)
        tokenized = [t[0] for t in tok.pos(s) if t[1] in tok.include_poses]
        nonum = re_nonum.findall(s)
        all = re_all.findall(s)
        concat = Counter(tokenized + nonum + all)
        concat = sorted(concat, key=lambda x: concat[x], reverse=True)
        print('토크나이저:        ', tokenized)
        print('정규표현식_숫자제외: ', nonum)
        print('정규표현식_전체:    ', all)
        print('토큰후보들_통합:    ', concat, end='\n' + '-' * 50 + '\n')


def dart_main(top=30, savefile=False, bigram=False, tokenizers=['mecab']):
    dart = pd.read_pickle('data/dart.pickle')
    dart['REP_NO'] = dart['SYMBOL'].apply(lambda x: keypair_ko_repno.get(x))
    dart['NAME'] = dart['REP_NO'].apply(lambda x: keypair_names.get(x))
    dart = dart.dropna(inplace=False)
    corp = SimpleCorpus(dart, repno_col='REP_NO', text_col='CONTENTS', name_col='NAME')
    tokenized = dict()
    concat = [Counter() for _ in range(len(corp.texts))]
    for tokenizer_name in tokenizers:
        tokenized[tokenizer_name] = get_keywords_df(corp, tokenizer=tokenizer_name, top=None, metric='freq',
                                                    return_type='counter', bigram=bigram)
        concat = concat_counters_lists(concat, tokenized[tokenizer_name])

    corp.counted_matrix = [ct.most_common(300) for ct in concat]
    top_words = [', '.join(
        [t[0] for t in lemm if not is_stopwords(t[0])][:top]
    ) for lemm in corp.counted_matrix]
    df = pd.DataFrame(data={
        'REP_NO': corp.repnos,
        'COMPANY': corp.names,
        'TOP_WORDS': top_words
    })
    if savefile:
        df.to_excel('tokenized/dart_keywords.xlsx', encoding='cp949')
    return df


def is_stopwords(word: str):
    conditions = [
        not biz_stopwords_hash.get(word),
        not word.isdigit(),
        not tok.stopwords.get(word) and len(word) > 1

    ]
    return sum(conditions) != len(conditions)


def concat_counters_lists(ct1: list, ct2: list):
    result = []
    for i1, i2 in zip(ct1, ct2):
        assert isinstance(i1, Counter)
        assert isinstance(i2, Counter)
        result.append(i1 + i2)
    return result


if __name__ == '__main__':
    path = 'tokenized/dart_freq_all.xlsx'
    biz_stopwords = get_korean_biz_stopwords(path)
    biz_stopwords_hash = {word: 1 for word in biz_stopwords}
    eng_stopwords_hash = {k: 1 for k in eng_stopwords}

    tokenizer_name = 'mecab'
    tok = KoreanTokenizer(tokenizer_name)

    kp = get_keypair()
    keypair_ko_repno = {symbol.split('.')[0]: repno for symbol, repno in zip(kp['SYMBOL'], kp['REP_NO']) if
                        symbol.endswith('KS') or symbol.endswith('KQ')}
    keypair_ko_repno.update({symbol: repno for symbol, repno in zip(kp['SYMBOL'], kp['REP_NO']) if
                             symbol.endswith('KS') or symbol.endswith('KQ')})
    keypair_names = {repno: name for repno, name in zip(kp['REP_NO'], kp['CMP_NM_ENG'])}

    re_all = re.compile('[가-힇|a-z|A-Z|\d|-]+')
    re_nonum = re.compile('[가-힇|a-z|A-Z|-]+')
    re_nonum_nohyphen = re.compile('[가-힇|a-z|A-Z]+')

    dart_main(top=100, savefile=True, bigram=True)
    print()
