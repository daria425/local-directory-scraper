from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

driver_path='/usr/local/bin/chromedriver'
url='https://findyour.islington.gov.uk/kb5/islington/directory/results.action?communitychannelnew=1'
service=Service(driver_path)
chrome_options=Options()
chrome_options.add_argument("--headless=new")

driver=webdriver.Chrome(options=chrome_options, service=service)


def scrape(url, title_xpath, selenium_driver, save_output=False):
    time.sleep(2)
    selenium_driver.get(url)
    content=selenium_driver.page_source
    if title_xpath is not None:
        content_title=selenium_driver.find_element(By.XPATH, title_xpath)
        content_title=content_title.text
    else: 
        content_title=driver.title
    if save_output:
        with open('output.html', 'w', encoding='utf-8') as file:
            file.write(content)
    return content, content_title


url="https://cindex.camden.gov.uk/kb5/camden/cd/results.action?communitychannel=2-10"
