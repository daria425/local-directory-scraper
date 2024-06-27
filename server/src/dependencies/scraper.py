from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scraper:
    def __init__(self):
        self.driver = None
        self.prefixes = {
            "camden": "https://cindex.camden.gov.uk/kb5/camden/cd/", 
            "islington": "https://findyour.islington.gov.uk/kb5/islington/directory/"
        }
    
    def get_category_directory_url(self, region):
        return self.prefixes[region] + "home.page"

    def create_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        return self.driver
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def scrape(self, url, save_output=False, wait_time=45):
        if self.driver is None:
            self.create_driver()
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, wait_time).until(EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#content')), 
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#page-content'))
            )) # Adjust this selector as needed
            content = self.driver.page_source
            content_title = self.driver.title

            if save_output:
                with open('output.html', 'w', encoding='utf-8') as file:
                    file.write(content)
        except TimeoutException:
            print(f"TimeoutException: The page at {url}did not load within {wait_time} seconds.")
            content, content_title = None, None
        except WebDriverException as e:
            print(f"WebDriverException: {e}")
            content, content_title = None, None
            self.close_driver()
        
        return content, content_title
    
    def get_category_page(self, region):
        category_page_url = self.get_category_directory_url(region)
        html = self.scrape(category_page_url)[0]
        return html
    
    def __enter__(self):
        self.create_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_driver()

        


                
