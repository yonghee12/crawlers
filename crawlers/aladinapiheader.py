
s = """Connection: keep-alive
Accept: */*
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36
X-Requested-With: XMLHttpRequest
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=247905989&start=main
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9"""
c = """Cookie: ACEUCI=1; CheckSameSite=IsValidSameSiteSet; AladdinUser=UID=-39544793&SID=v0ooNUc2IIDmn3bRAH74yQ%3d%3d; AladdinSession=UID=-39544793&SID=v0ooNUc2IIDmn3bRAH74yQ%3d%3d; AladdinUS=pFWyGmidf7yeUny5ns2o8g%3d%3d&USA=0; ACEUACS=1599638213479144627; ACEFCID=UID-5F588AC5480E0E1FE3755CE8; _ga=GA1.3.1051784358.1599638214; _gid=GA1.3.1828051194.1599638214; _BS_GUUID=u2HuL6EWGuADCh0mRnGr5Gd87NmiB3R65zAQGeMm; _TRK_AUIDA_13987=3f2604803b20fe6a60109d4e66020f3f:1; _TRK_ASID_13987=c0564da316cc2542bed20bd60ab20a00; AUAZ3A43579=1599638344219466998%7C2%7C1599638344219466998%7C1%7C1599638344808ZVXCHZ; ARAZ3A43579=httpswwwaladincokrmmproductaspxItemId247905989httpswwwaladincokrmmainaspx; ASAZ3A43579=1599638344219466998%7C1599638424381976142%7C1599638344219466998%7C0%7Chttpswwwgooglecom; divGoodsEventBottomLayerCount=2; refererURL=https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=247905989&start=main; _gat_gtag_UA_59266_2=1"""

sss = [ss.split(': ') for ss in s.split('\n')]
headers = {k: v for k, v in sss}

cookies = {}
for cook in [cc.split("=") for cc in c.split("; ")]:
    cookies.update({cook[0]: '='.join(cook[1:])})
