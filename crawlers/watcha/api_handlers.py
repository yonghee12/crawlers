from crawlers.watcha.functions import *


class WatchaApiHandler:
    _URL_HEAD = 'https://api-pedia.watcha.com/api/'

    def __init__(self, mod=6, default_wait=6.1, max_attempt=3):
        self.wait_cond = lambda i: i != 1 and i % mod == 1
        self.max_attempt = max_attempt
        self.default_wait_sec = default_wait

        self._total = 0
        self._api_head = None
        self._keys = None
        self._name_convention = None

    def get(self):
        raise NotImplementedError

    def _get(self, url_head, max_page, verbose=1, n_max=1e9, print_col=None):
        df = pd.DataFrame()
        for page in range(1, max_page + 1):
            url = url_head + f"&page={page}&size=20"
            result = self._get_one_loop(url, page, n_max=n_max)
            if result is None:
                return df
            else:
                df_local = pd.json_normalize(result)
                df = df.append(df_local)
                time.sleep(self._get_transition_sec())
                if verbose > 0:
                    if not print_col:
                        print(df_local.iloc[0])
                    else:
                        print(set(list(df_local[print_col])))
            self._total = len(df)
        self.reset_total()
        return df

    def _get_one_loop(self, api_url, i, attempt=1, n_max=1e9):
        wait = self._get_wait_time(i, attempt)
        if wait > 1:
            print(f'Waiting for {wait} sec. Retrieved: {self._total}')
            time.sleep(wait)
        result = get_api_result(api_url)
        if result:
            return result
        else:
            print(f"No Results. | retrieved: {self._total}, n_max: {n_max}")
            if attempt >= self.max_attempt or self._total >= n_max:
                print("Stop Attempt.")
                return None
            return self._get_one_loop(api_url, i, attempt=attempt + 1, n_max=n_max)

    def _get_wait_time(self, i, attempt):
        if attempt > 1:
            return self.default_wait_sec + attempt - 1
        elif self.wait_cond(i):
            return self.default_wait_sec
        elif i == 1:
            return 1
        else:
            return 0

    def reset_total(self):
        self._total = 0

    def _get_transition_sec(self):
        # return 0.1 + random.random() / 2
        return 0.01

    def _save_df(self, df, info):
        directory = os.path.join(ROOT_DIR, 'results')
        if not os.path.exists(directory):
            os.mkdir(directory)
        df.reset_index(inplace=True, drop=True)
        filepath = os.path.join("results", f'{self._name_convention}_{info}_len{len(df)}.csv')
        path = os.path.join(ROOT_DIR, filepath)
        df.to_csv(path)

    def get_keys(self):
        return self._keys


class WatchaMetadataHandler(WatchaApiHandler):
    def __init__(self, mod=6, default_wait=6.1, max_attempt=3):
        super().__init__(mod, default_wait, max_attempt)
        self._api_head = api_headers['evaluation']
        self._keys = list(evaluation_ids.keys())
        self._name_convention = "watcha_eval"

        self.api_keys_set = set(self._keys)

    def get(self, max_page, category=None, verbose=1, save=False):
        assert category in self.api_keys_set
        url_head = self._URL_HEAD + self._api_head + evaluation_ids[category]
        df = self._get(url_head, max_page, verbose)
        if save:
            self._save_df(df, category)
        return df


class WatchaCommentsHandler(WatchaApiHandler):
    def __init__(self, mod=6, default_wait=6.1, max_attempt=3):
        super().__init__(mod, default_wait, max_attempt)
        self._api_head = None
        self._keys = list(evaluation_ids.keys())
        self._name_convention = "watcha_eval"

        self.api_keys_set = set(self._keys)

    def get(self, content_id, order='popular', verbose=1, print_col=None, title_to_save_df=None):
        url_head = f'https://api-pedia.watcha.com/api/contents/{content_id}/comments?filter=all&order={order}'
        n_min, n_max = get_n_comments(content_id)
        if n_min == 0 and n_max == 0:
            return None
        print(f"n_max_commnets: {n_max}")

        df = self._get(url_head, n_max // 20 + 2, verbose, n_max, print_col=print_col)
        if title_to_save_df:
            self._save_df(df, title_to_save_df)
        return df


if __name__ == '__main__':
    # api = WatchaMetadataHandler(max_attempt=3)
    # api.get(max_page=1000, category='역대 100만 관객 돌파 영화', verbose=1)
    filepath = os.path.join(PROJECT_ROOT, "results/watcha_eval_전문가 고평점 영화_len100.csv")
    meta = pd.read_csv(filepath, index_col=0)
    row = meta.iloc[0]
    api = WatchaCommentsHandler()
    api.get(row['title'], row['code'], order='popular')
    # api.api_keys_set
    # print()
