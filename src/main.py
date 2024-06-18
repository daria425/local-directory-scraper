from info_extraction.scrape import scrape, driver
from info_extraction.read_html import create_df, get_last_page
import pandas as pd

url=f"https://findyour.islington.gov.uk/kb5/islington/directory/results.action?communitychannelnew=12"
dataframes=[]

selenium_driver=driver



def get_islington_data(url):
    html, page_title=scrape(url, selenium_driver)
    last_page=get_last_page(html)
    first_page_df=create_df(html)
    dataframes.append(first_page_df)

    if last_page is not None:
        inc=50
        for i in range(50, int(last_page)+inc, inc):
            url_to_scrape=f"{url}&sr={i}"
            html=scrape(url_to_scrape, selenium_driver)[0]
            df=create_df(html)
            dataframes.append(df)

    selenium_driver.quit()
    combined_dfs=pd.concat(dataframes, axis=0, ignore_index=True)
    csv=combined_dfs.to_csv(f'{page_title}.csv')

