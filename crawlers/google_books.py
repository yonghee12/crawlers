import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class GoogleBookCrawler:
    def __init__(self, driver_path):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
        self.iddict = {}

    def close(self):
        self.driver.quit()

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
        lasttext = ''
        for i in range(200):

            try:
                # element = WebDriverWait(driver, 3).until(
                #     ec.presence_of_element_located((By.CLASS_NAME, 'gb-page-root')))

                WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.CLASS_NAME, 'gb-page-root')))

            except Exception as e:
                print(str(e))
                break

            finally:
                html = driver.page_source
                bs = BeautifulSoup(html, 'lxml')
                tags = bs.findAll('div', attrs={'class': 'gb-content'})

                text = ""
                for tag in tags:
                    text += tag.text.replace("\n\n", "").replace("\n", " ").replace("\'", "").replace("\"", "")

                if not text:
                    print('trying one more time..')
                    time.sleep(1)
                    html = driver.page_source
                    bs = BeautifulSoup(html, 'lxml')
                    tags = bs.findAll('div', attrs={'class': 'gb-content'})

                    text = ""
                    for tag in tags:
                        text += tag.text.replace("\n\n", "").replace("\n", " ").replace("\'", "").replace("\"", "")

                driver.find_element_by_css_selector('.gb-pagination-controls-right').click()

                if text:
                    texts = text.replace('\xa0', ' ').replace('\u200b', '')
                    texts = re.sub("[\n]+", "\n", texts)
                    texts = re.sub("[ ]+", " ", texts)

                    if not lasttext == texts:
                        print(f"page: {i}, text: {texts}")
                        res.append((i, texts))
                        lasttext = texts
                else:
                    print(f"page: {i}, nothing here.")

        return res


if __name__ == "__main__":
    yonghee_local_path = '/Users/yonghee/chromedriver'
    gc = GoogleBookCrawler(yonghee_local_path)
    r = gc.crawlBook('KYcsCAAAQBAJ')
    print(r)
