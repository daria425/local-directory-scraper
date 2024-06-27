
from .content_reader import CamdenContentReader, IslingtonContentReader
from .scraper import Scraper
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException

def make_category_csv(url, region):
    dataframes = []

    with Scraper() as scraper:
        html, content_title = scraper.scrape(url)
        if region.lower() == "camden":
            camden_reader = CamdenContentReader(html)
            last_page = camden_reader.get_last_page()

            first_page_df = camden_reader.create_df()
            dataframes.append(first_page_df)
            if last_page is not None:
                inc = 10
                for i in range(10, inc + int(last_page), inc):
                    new_url = f"{url}&sr={i}&nh=10"
                    success = False
                    retries = 3
                    while not success and retries > 0:
                        try:
                            # Close and restart the scraper for each request
                            scraper.close_driver()
                            scraper.create_driver()
                            print(f"Scraping URL: {new_url}")
                            html = scraper.scrape(new_url)[0]
                            df = CamdenContentReader(html).create_df()
                            dataframes.append(df)
                            success = True
                        except TimeoutException as e:
                            print(f"TimeoutException: {e}")
                            retries -= 1
                            if retries > 0:
                                print(f"Retrying... {retries} attempts left.")
                                time.sleep(5)  # Wait before retrying
                            else:
                                print(f"Failed to load page: {new_url} after multiple attempts.")
                                break
                        except Exception as e:
                            print(f"Unexpected exception: {e}")
                            break
        elif region.lower() == "islington":
            islington_reader = IslingtonContentReader(html)
            last_page = islington_reader.get_last_page()
            print(last_page)
            first_page_df = islington_reader.create_df()
            dataframes.append(first_page_df)
            if last_page is not None:
                inc = 50
                for i in range(50, int(last_page) + inc, inc):
                    new_url = f'{url}&sr={i}'
                    success = False
                    retries = 3
                    while not success and retries > 0:
                        try:
                            # Close and restart the scraper for each request
                            scraper.close_driver()
                            scraper.create_driver()
                            print(f"Scraping URL: {new_url}")
                            html = scraper.scrape(new_url)[0]
                            df = IslingtonContentReader(html).create_df()
                            print("df made")
                            dataframes.append(df)
                            success = True
                        except TimeoutException as e:
                            print(f"TimeoutException: {e}")
                            retries -= 1
                            if retries > 0:
                                print(f"Retrying... {retries} attempts left.")
                                time.sleep(5)  # Wait before retrying
                            else:
                                print(f"Failed to load page: {new_url} after multiple attempts.")
                                break
                        except Exception as e:
                            print(f"Unexpected exception: {e}")
                            break

    combined_dfs = pd.concat(dataframes, axis=0, ignore_index=True)
    print((f'csv with title {content_title}.csv will be made'))
    return combined_dfs
                         





