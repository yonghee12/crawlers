from selenium import webdriver

options = webdriver.FirefoxOptions()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
options.set_preference("browser.download.dir", "/pdf")
options.set_preference("pdfjs.disabled", True)
driver = webdriver.Firefox(executable_path='/Users/ryan/geckodriver', firefox_options=options)

url = 'http://consensus.hankyung.com/apps.analysis/analysis.downpdf?report_idx=557012'
driver.get(url)
driver.find_element_by_css_selector('#download').click()
print()
