from crawlers.watcha.functions import *


class WatchaMetadataHandler:
    _DEFAULT_WAIT_SEC = 6.1
    _URL_HEAD = 'https://api-pedia.watcha.com/api'
    _WAIT_COND = lambda self, i: i != 1 and i % 6 == 1

    def __init__(self, max_attempt):
        self._MAX_ATTEMPT = 3
        pass

    def get(self, category, mx, verbose=1):
        df = pd.DataFrame()
        url_head = eval_links[category]
        for i in range(1, mx + 1):
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
            print(i, f'Waiting for {wait} sec.')
            time.sleep(wait)
        result = get_eval_result(api_url)
        if result:
            return result
        else:
            print("No Results")
            if attempt >= self._MAX_ATTEMPT:
                print("Stop Attempt.")
                return None
            return self._get_one_loop(api_url, i, attempt + 1)

    def _get_wait_time(self, i, attempt):
        if attempt > 1:
            return self._DEFAULT_WAIT_SEC + attempt
        elif self._WAIT_COND(i):
            return self._DEFAULT_WAIT_SEC
        elif i == 1:
            return 1
        else:
            return 0

    def _get_transition_sec(self):
        # return 0.1 + random.random() / 2
        return 0.1

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


if __name__ == '__main__':
    api = WatchaMetadataHandler(max_attempt=3)
    api.get('역대 100만 관객 돌파 영화', 1000, verbose=1)
    print()