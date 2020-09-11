from urllib import parse


from seleniumwire import webdriver

options = webdriver.FirefoxOptions()

xpaths = {
    'stock-news': '/html/body/div[4]/div[2]/div/div/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]',
    'lastitem': '/html/body/div[4]/div[2]/div/div/div/div[2]/div/div/div/div/div/div[5]/div[2]/div[2]/div/div[1]/div[10]/div[1]/div[1]/div',
    'stock-4': '/html/body/div[4]/div[2]/div/div/div/div[2]/div/div/div/div/div/div[5]/div[2]/div[2]/div/div[2]/div/div[4]'
}


def get_zacks_news_api_params(headless=True):
    options.headless = headless
    tokens_req = ['cse_tok', 'exp', 'callback']
    driver = webdriver.Firefox(executable_path='/Users/ryan/geckodriver', firefox_options=options)
    url = 'https://www.zacks.com/search.php?q=apple'
    driver.get(url)
    driver.implicitly_wait(1)
    driver.find_element_by_xpath(xpaths['stock-news']).click()
    driver.implicitly_wait(1)
    lastitem = driver.find_element_by_xpath(xpaths['lastitem'])
    lastitem.location_once_scrolled_into_view
    driver.find_element_by_xpath(xpaths['stock-4']).click()

    internal_requests = driver.requests
    driver.quit()
    req = [req for req in internal_requests if req.path.startswith("https://cse.google.com/cse/element/v1")]
    if req:
        query_str = parse.urlparse(req[-1].path).query
        query_dic = parse.parse_qs(query_str)
        print(query_dic)
        return query_dic


get_zacks_news_api_params(headless=True)
# get_zacks_news_api_params(headless=False)
