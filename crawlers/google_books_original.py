import asyncio
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from bs4 import BeautifulSoup

import time


class GoogleBookCrawler:
    def __init__(self):

        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        yonghee_local_path = '/Users/yonghee/chromedriver'
        self.driver = webdriver.Chrome(yonghee_local_path, chrome_options=chrome_options)
        self.iddict = {}

    def crawlBook(self, bookId):
        # driver.set_window_size(1920, 1080)
        # driver.implicitly_wait(0)

        driver = self.driver
        start = time.time()
        url = f'https://play.google.com/books/reader?id={bookId}&hl=ko'
        print(url)

        driver.get(url)
        driver.switch_to.frame(":0.reader")
        text = ""
        cnt = 0

        res = []

        for i in range(200):

            try:
                element = WebDriverWait(driver, 3).until(
                    ec.presence_of_element_located((By.CLASS_NAME, 'gb-page-root')))

            except Exception as inst:
                break

            finally:
                html = driver.page_source
                bs = BeautifulSoup(html, 'html.parser')
                tags = bs.findAll('div', attrs={'class': 'gb-content'})
                text = ""
                for tag in tags:
                    text += tag.text.replace("\n\n", "").replace("\n", " ").replace("\'", "").replace("\"", "")

                driver.find_element_by_css_selector('.gb-pagination-controls-right').click()
                res.append((i, text))

        print(res)
        return res


if __name__ == "__main__":
    gc = GoogleBookCrawler()
    r = gc.crawlBook('KYcsCAAAQBAJ')
    print(r)
