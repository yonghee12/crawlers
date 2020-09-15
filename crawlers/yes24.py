import requests
from header import *
import requests

cookies = {
    'YES24_MF_FP': '94c7c84c81451dab46b49dee78001564',
    'RecentViewGoods': '',
    'RecentViewInfo': 'NotCookie%3DY%26Interval%3D5%26ReloadTime%3DTue%2C%2015%20Sep%202020%2002%3A08%3A02%20GMT%26First%3Dtrue',
    '__utma': '12748607.1441316326.1600133668.1600133668.1600135675.2',
    '__utmb': '12748607.3.10.1600135675',
    '__utmc': '12748607',
    '__utmz': '12748607.1600133668.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'BLOG_URL': '',
    'CART_NO': '',
    'ClientIPAddress': '',
    'EntLoginInfo': 'c3VuY2FyMTAwMHwyMDIwLTA5LTE1IDExOjA4OjAy',
    'FAMILY_PAY_NO': '',
    'MEM_AGE': '',
    'MEM_GB': '',
    'MEM_ID': '',
    'MEM_NM': '',
    'MEM_NO': '',
    'NEW_PID': '',
    'NICK_NM': '',
    'ServerIPAddress': '',
    'ServiceCookies': 'MTQ2OTc3MzZgc3VuY2FyMTAwMGDDtb/ryPFgMGAwMWBzdW5jYXIxMDAwYGAxNDY5NzczNmAyNmBkb1kzUTJ3UC9jYW1RMEdMMkZUS0JxRm1aemc4eDNpa2pkcXBrRlBDVFMrUlVFdWwrb2hCL0FmQ0t6aW0wQUJadXlZTU5QeUFrOHZ0bWorWTNpalk2Zz09YC9jM2JZSGd4eXFBM2xDakplT2lURDlCYTlxOGhyOWlGWm5xS3ZGUkJVQkVMcjR4MGVzUEtHQ1RsMTh0OUpnZ0VQT2pWQ1ZnczVSTldpTWdDZExQMCs2SWNaaDE2MTJXVU94Y0c5WitaOWxSV3Jnbk11M29JdVZtdXJ1SGtBOFlyRm1qK01hN1ZHcGJjcEVDRXRqT2gwUFRmY3FDUFdBVGEzckdUQlhzQ3FKST1gb2ZTc2VHakVRc2ZrQXgrZjBpSy9oZz09',
    'WiseLogParam': 'c3VuY2FyMTAwMA==',
    'wcs_bt': 's_1b6883469aa6:1600135683',
    '__utmt': '1',
    'HTTP_REFERER': 'https://www.yes24.com/Templates/FTLogin.aspx',
    'PCID': '16001336673679667215134',
    'ASP.NET_SessionId': 'ak35srwkc15untvoq3zys3m5',
    'yes24_glbola_redirect': 'validationcheck=true|nation_id=south korea',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.yes24.com',
    'Content-Length': '498',
    'Accept-Language': 'en-us',
    'Host': 'www.yes24.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
    'Referer': 'https://www.yes24.com/Templates/FTLogin.aspx',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

data = {
  'FBLoginSub$hdfLoginToken': 'jj+Q9vDc35+txh6eAqGPaPd0ydRR6Q7bWVw76hBmVqpz99NiRHND3fRUbyZKDQim',
  'FBLoginSub$hdfLoginHash': 'MTYwMDEzNjAzNTk4MHxqaitROXZEYzM1K3R4aDZlQXFHUGFQZDB5ZFJSNlE3YldWdzc2aEJtVnFwejk5TmlSSE5EM2ZSVWJ5WktEUWlt',
  'LoginType': '',
  'FBLoginSub$ReturnURL': '',
  'FBLoginSub$ReturnParams': '',
  'RefererUrl': 'https://www.yes24.com/Main/default.aspx',
  'AutoLogin': '1',
  'LoginIDSave': 'N',
  'FBLoginSub$NaverCode': '',
  'FBLoginSub$NaverState': '',
  'FBLoginSub$Facebook': '',
  'SMemberID': 'suncar1000',
  'SMemberPassword': 'cjsdydgml1!'
}

session = requests.Session()
res = session.post('https://www.yes24.com/Templates/FTLogin.aspx', headers=headers, cookies=cookies, data=data)
res.text
# response = requests.post('https://www.yes24.com/Templates/FTLogin.aspx', headers=headers, cookies=cookies, data=data)
# response.text

session.get('https://ssl.yes24.com/MyPageOrderList/MyPageOrderList')