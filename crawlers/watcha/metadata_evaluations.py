from crawlers.watcha.functions import *


class WatchaApiHandler:
    _URL_HEAD = 'https://api-pedia.watcha.com/api/'

    def __init__(self, mod=6, default_wait=6.1, max_attempt=3):
        self.wait_cond = lambda i: i != 1 and i % mod == 1
        self.max_attempt = max_attempt
        self.default_wait_sec = default_wait

        self.api_head = None
        self.api_keys_set = None

        self.api_head = api_headers['evaluation']
        self._keys = list(evaluation_ids.keys())
        self.api_keys_set = set(self._keys)

    def get(self, category, max_page, verbose=1):
        assert category in self.api_keys_set
        url_head = self._URL_HEAD + self.api_head + evaluation_ids[category]
        df = pd.DataFrame()
        for i in range(1, max_page + 1):
            url = url_head + f"&page={i}&size=20"
            result = self._get_one_loop(url, i)
            if result is None:
                break
            else:
                df = df.append(pd.json_normalize(result))
                time.sleep(self._get_transition_sec())
                if verbose > 0:
                    self._print_results(i, result)
        self._save_df(df, category)
        return df

    def _get_one_loop(self, api_url, i, attempt=1):
        wait = self._get_wait_time(i, attempt)
        if wait > 1:
            print(f'Waiting for {wait} sec.')
            time.sleep(wait)
        result = get_eval_result(api_url)
        if result:
            return result
        else:
            print("No Results")
            if attempt >= self.max_attempt:
                print("Stop Attempt.")
                return None
            return self._get_one_loop(api_url, i, attempt + 1)

    def _get_wait_time(self, i, attempt):
        if attempt > 1:
            return self.default_wait_sec + attempt - 1
        elif self.wait_cond(i):
            return self.default_wait_sec
        elif i == 1:
            return 1
        else:
            return 0

    def _get_transition_sec(self):
        # return 0.1 + random.random() / 2
        return 0.01

    def _print_results(self, i, result):
        print(i, [r.get('title') for r in result])

    def _save_df(self, df, category):
        directory = os.path.join(ROOT_DIR, 'results')
        if not os.path.exists(directory):
            os.mkdir(directory)
        df.reset_index(inplace=True, drop=True)
        filepath = os.path.join("results", f'watcha_eval_{category}_len{len(df)}.csv')
        path = os.path.join(ROOT_DIR, filepath)
        df.to_csv(path)

    @classmethod
    def keys(cls):
        return cls._KEYS


class WatchaMetadataHandler(WatchaApiHandler):
    _URL_HEAD = 'https://api-pedia.watcha.com/api/'

    def __init__(self, mod=6, default_wait=6.1, max_attempt=3):
        super().__init__(mod, default_wait, max_attempt)
        self.api_head = api_headers['evaluation']
        self._keys = list(evaluation_ids.keys())
        self.api_keys_set = set(self._keys)

    def get(self, category, max_page, verbose=1):
        assert category in self.api_keys_set
        url_head = self._URL_HEAD + self.api_head + evaluation_ids[category]
        df = pd.DataFrame()
        for i in range(1, max_page + 1):
            url = url_head + f"&page={i}&size=20"
            result = self._get_one_loop(url, i)
            if result is None:
                break
            else:
                df = df.append(pd.json_normalize(result))
                time.sleep(self._get_transition_sec())
                if verbose > 0:
                    self._print_results(i, result)
        self._save_df(df, category)
        return df

    def _get_one_loop(self, api_url, i, attempt=1):
        wait = self._get_wait_time(i, attempt)
        if wait > 1:
            print(f'Waiting for {wait} sec.')
            time.sleep(wait)
        result = get_eval_result(api_url)
        if result:
            return result
        else:
            print("No Results")
            if attempt >= self.max_attempt:
                print("Stop Attempt.")
                return None
            return self._get_one_loop(api_url, i, attempt + 1)

    def _get_wait_time(self, i, attempt):
        if attempt > 1:
            return self.default_wait_sec + attempt - 1
        elif self.wait_cond(i):
            return self.default_wait_sec
        elif i == 1:
            return 1
        else:
            return 0

    def _get_transition_sec(self):
        # return 0.1 + random.random() / 2
        return 0.01

    def _print_results(self, i, result):
        print(i, [r.get('title') for r in result])

    def _save_df(self, df, category):
        directory = os.path.join(ROOT_DIR, 'results')
        if not os.path.exists(directory):
            os.mkdir(directory)
        df.reset_index(inplace=True, drop=True)
        filepath = os.path.join("results", f'watcha_eval_{category}_len{len(df)}.csv')
        path = os.path.join(ROOT_DIR, filepath)
        df.to_csv(path)

    def keys(self):
        return self._keys


if __name__ == '__main__':
    api = WatchaMetadataHandler(max_attempt=3)
    api.get('역대 100만 관객 돌파 영화', 1000, verbose=1)
    print()
