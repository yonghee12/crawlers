import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from matplotlib import pyplot as plt

okt = pd.read_excel('tokenized/result_okt.xlsx', header=0, index_col=None, encoding='utf8')
mecab = pd.read_excel('tokenized/result_mecab.xlsx', header=0, index_col=None, encoding='utf8')

mecab = mecab.drop_duplicates('word', keep='first')
okt = okt.drop_duplicates('word', keep='first')


def normalize(arr: pd.Series or np.ndarray, logarize=False, from_zero=False) -> pd.Series:
    assert isinstance(arr, pd.Series) or isinstance(arr, np.ndarray)
    x_arr = pd.Series(arr) if not logarize else pd.Series(np.log(arr))
    x_bar = x_arr.mean(axis=0)
    std = x_arr.std(axis=0)
    x_normalized = (x_arr - x_bar) / std
    x_normalized = x_normalized - x_normalized.min() if from_zero else x_normalized
    return x_normalized


okt_c = normalize(okt['count'], logarize=True, from_zero=True)
normalize(okt['count'], logarize=True, from_zero=False)
mecab_c = normalize(mecab['count'], logarize=True, from_zero=True)

okt['count'] = okt_c
mecab['count'] = mecab_c

merge_options = {
    'how': 'outer',
    'left': okt.drop('pos', axis=1, inplace=False),
    'right': mecab.drop('pos', axis=1, inplace=False),
    'on': 'word',
    'suffixes': ('_okt', '_mecab')
}
merged = pd.merge(**merge_options)
merged: pd.DataFrame
merged = merged.fillna(value=0)
merged['score'] = merged['count_okt'] * 0.5 + merged['count_mecab'] * 0.5
merged = merged.sort_values(by='score', ascending=False)
merged.to_excel('tokenized/count_score.xlsx')