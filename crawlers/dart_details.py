import pandas as pd
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920*1024')
options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR")
options.add_argument("disable-infobars")
driver = webdriver.Chrome('/Users/ryan/chromedriver', chrome_options=options)

driver.get('http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20200413800348')
driver.switch_to.frame('ifrm')
tables = driver.find_elements_by_tag_name('table')
table = tables[1]
table_html = table.get_attribute('outerHTML')
df = pd.read_html(table_html)[0]
