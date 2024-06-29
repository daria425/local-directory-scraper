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
        self.prefixes = {
            "camden": "https://cindex.camden.gov.uk/kb5/camden/cd/", 
            "islington": "https://findyour.islington.gov.uk/kb5/islington/directory/"
        }
        self.cache = {}

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
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        return driver

    def scrape(self, url, save_output=False, wait_time=45):
        if url in self.cache:
            print(f"Returning cached content for {url}")
            return self.cache[url]
        
        driver = self.create_driver()
        try:
            driver.get(url)
            WebDriverWait(driver, wait_time).until(EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#content')), 
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#page-content'))
            ))  # Adjust this selector as needed
            content = driver.page_source
            content_title = driver.title

            if save_output:
                with open('output.html', 'w', encoding='utf-8') as file:
                    file.write(content)
        except TimeoutException:
            print(f"TimeoutException: The page at {url} did not load within {wait_time} seconds.")
            content, content_title = None, None
        except WebDriverException as e:
            print(f"WebDriverException: {e}")
            content, content_title = None, None
        finally:
            driver.quit()
        
        self.cache[url] = (content, content_title)
        return content, content_title
