from info_extraction.scrape import scrape, driver
from info_extraction.read_html import create_df, get_last_page
import pandas as pd

url=f"https://cindex.camden.gov.uk/kb5/camden/cd/results.action?communitychannel=7-1"
dataframes=[]

selenium_driver=driver



def get_islington_data(url):
    html, page_title=scrape(url, "//*[@id=\"content\"]/div/h1",selenium_driver)
    last_page=get_last_page(html, "islinton")
    first_page_df=create_df(html, "islington")
    dataframes.append(first_page_df)

    if last_page is not None:
        inc=50
        for i in range(50, int(last_page)+inc, inc):
            url_to_scrape=f"{url}&sr={i}"
            html=scrape(url_to_scrape, selenium_driver)[0]
            df=create_df(html, "islington")
            dataframes.append(df)

    selenium_driver.quit()
    combined_dfs=pd.concat(dataframes, axis=0, ignore_index=True)
    combined_dfs.to_csv(f'{page_title}.csv')

def get_camden_data(url, selenium_driver):
    html, page_title=scrape(url, None, selenium_driver=selenium_driver)
    last_page=get_last_page(html, "camden")
    first_page_df=create_df(html, "camden")
    dataframes.append(first_page_df)
    if last_page is not None:
        inc=10
        for i in range(10, int(last_page)+inc,inc):
            url_to_scrape=f'{url}&sr={i}&nh=10'
            print(url_to_scrape)
            html=scrape(url_to_scrape, None,  selenium_driver)[0]
            df=create_df(html, "camden")
            dataframes.append(df)

    selenium_driver.quit()
    combined_dfs=pd.concat(dataframes, axis=0, ignore_index=True)
    combined_dfs.to_csv(f'{page_title}.csv')

get_camden_data(url, selenium_driver)

