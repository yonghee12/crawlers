import requests
import time
from importlib import reload


def make_query_f_string(column_list):
    return ', '.join([f"\"{{row['{col}']}}\"" for col in column_list])


def get_safe(url, headers=None, cookies=None, max_errors=2, rtype='text', error=0, ):
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
    except Exception as e:
        if error > max_errors:
            return ''
        print(str(e), 'RELOADING REQUESTS MODULE')
        reload(requests)
        time.sleep(2)
        return get_safe(url, headers, cookies, max_errors, rtype, error + 1)
    else:
        if response.status_code == 200:
            if rtype == 'text':
                return response.text
            elif rtype == 'content':
                return response.content
        return ''
