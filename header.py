def get_headers_from_str(header_str):
    sss = [ss.split(': ') for ss in header_str.split('\n') if ss.strip()]
    return {k.replace(":", ""): v for k, v in sss}


def get_cookies_from_str(cookie_str):
    cookies = {}
    for cook in [cc.split("=") for cc in cookie_str.split("; ") if cc.strip()]:
        cookies.update({cook[0]: '='.join(cook[1:])})
    return cookies


ALADIN_HEADERS = {'Connection': 'keep-alive', 'Accept': '*/*', 'Sec-Fetch-Dest': 'empty',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                  'X-Requested-With': 'XMLHttpRequest', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors',
                  'Referer': 'https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=247905989&start=main',
                  'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9'}

WATCHA_HEADERS = {'accept': 'application/vnd.frograms+json;version=20',
                  'accept-encoding': 'gzip, deflate, br',
                  'accept-language': 'en-US,en;q=0.9,ko;q=0.8,ko-KR;q=0.7',
                  'origin': 'https://pedia.watcha.com',
                  'referer': 'https://pedia.watcha.com/ko-KR/contents/m5QA6GD/comments',
                  'sec-fetch-dest': 'empty',
                  'sec-fetch-mode': 'cors',
                  'sec-fetch-site': 'same-site',
                  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                  'x-watcha-client': 'watcha-WebApp',
                  'x-watcha-client-language': 'ko',
                  'x-watcha-client-region': 'KR',
                  'x-watcha-client-version': '2.0.0'}

WATCHA_COOKIES = {'fbm_126765124079533': 'base_domain=.watcha.com',
                  '_s_guit': '6011cddaa146d8636c21057cea10ddb0a564b30d1eb62c51151d47e0433a',
                  '_gid': 'GA1.2.276962436.1599791163',
                  'fbsr_126765124079533': 'uAPg6vyLGVYRo_ESHHqpwbX8ObLuFmnvXpGe3kkAl6I.eyJ1c2VyX2lkIjoiMTAwMDAxOTUzMDgwOTc2IiwiY29kZSI6IkFRQXRIbUJnMXVGMkp5am9NcjRUa0pIT2NfWVFiT2VfUnQ0LTVRUUVKRktxMEkwWHV5VTB5WXJjODF3T0ozWVNHUE4wQXhHUWVXQUVydlhBYmUxbFgwYS0zNzdVR09fZzQ0T3hETTBHN1FOc3ZxQnJFR0RwTzQtbHdfWW9PZkI2T2lIVjJQZk9zMWstejgyRnRUS0FZUHNqdG9XVXNEWTFnTF9qNnRIZEhoTnMyNy15ZUdFS3VvZ2FjLW1USzkwZUN6S1QwU0dpUHNLeE9nN1Z5RmhYcEc2NGVkb1F1QzRwMzJDVDFyNklUSjUxNW53RW90dXprVzlnbzhXMDhtc0o5dF9vc1hTUVlaY2hvZ214eDdIQ0pWcWxHQlFNOWxIaHdWY0dxdHRxQ3YxTUpPOGdWYUNhdk9kcHZiMTZld0hLU2czRmYybFN3dkdBTmEwbjEtRnpSTFlvZlBFcDZ2Mk9pMFZvWkdsQ0l2M2ZMdyIsIm9hdXRoX3Rva2VuIjoiRUFBQnpTczR3ejYwQkFFTXJLTDZkRXRIMXJDa2VpWkNaQmxQTXFQMUtCWGlNSVpDOUtPNlBBbjJVMDFDS0haQkZZdlpDRGlTUlZTTEtleVlsODRZR3M1NVEyc0c2ZzR3VGE0RnRHWkE0OG1DVzFETVhweFJwTnd0MmtpSnh0amRBVnBsZXpyWkNzYm1WYXNuVjdVNDdoQ2p1c09mMFdnZ005dW5Od3pEdjVMdGxVNHpDdWYxOVFTSWVaQ0txTlpBc1R2SHE0UzdEcDJkS2laQlFaRFpEIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE1OTk3OTExNjd9',
                  '_c_drh': 'true',
                  '_ga': 'GA1.1.789317587.1599791163',
                  '_ga_1PYHGTCRYW': 'GS1.1.1599791163.1.1.1599791637.0',
                  '_guinness_session': 'arCLiEn2XE5JYwnviP4k43pFljcUqLbC1kR%2F0evZbunmb48ZuZAd82fkZ65VTPcmnGARbhn6WuBA2X%2Bv7ekEz5TX--NRJ6gd9uvSo14qBd--Q4vrg37bKSwYr9rhJ9ihhA%3D%3D'}
