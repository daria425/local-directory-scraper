from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

class Scraper:
    def __init__(self):
        self.driver_path='/usr/local/bin/chromedriver'
        self.driver=None


    def create_driver(self):
        service=Service(self.driver_path)
        chrome_options=Options()
        chrome_options.add_argument("--headless=new")
        self.driver=webdriver.Chrome(options=chrome_options, service=service)
        return self.driver
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def scrape(self, url, save_output=False):
        time.sleep(2)
        driver=self.create_driver()
        driver.get(url)
        content=driver.page_source
        content_title=driver.title
        if save_output:
            with open('output.html', 'w', encoding='utf-8') as file:
             file.write(content)
        return content, content_title
    
    def __enter__(self):
        self.create_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_driver()
  

        


                
