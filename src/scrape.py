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

def scrape(url, save_output=False):
    time.sleep(2)
    driver.get(url)
    content=driver.page_source
    content_title=driver.find_element(By.XPATH, "//*[@id=\"content\"]/div/h1")
    print(content_title.text)
    driver.quit()
    if save_output:
        with open('output.html', 'w', encoding='utf-8') as file:
            file.write(content)
    return content

page_content=scrape(url)
