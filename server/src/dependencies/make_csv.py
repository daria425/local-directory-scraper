
from .content_reader import CamdenContentReader, IslingtonContentReader
from .scraper import Scraper
import pandas as pd

def make_category_csv(url, region):
    dataframes=[]
    with Scraper() as scraper:
        html, content_title=scraper.scrape(url)
        if region.lower()=="camden":
            camden_reader=CamdenContentReader(html)
            last_page=camden_reader.get_last_page()
       
            first_page_df=camden_reader.create_df()
            dataframes.append(first_page_df)
            if last_page is not None:
                inc=10
                for i in range(10, inc+int(last_page), inc):
                    new_url=f"{url}&sr={i}&nh=10"
                    html=scraper.scrape(new_url)[0]
                    df=CamdenContentReader(html).create_df()
                    dataframes.append(df)
        elif region.lower()=="islington":
            islington_reader=IslingtonContentReader(html)
            last_page=islington_reader.get_last_page()
            print(last_page)
            first_page_df=islington_reader.create_df()
            dataframes.append(first_page_df)
            if last_page is not None:
                inc=50
                for i in range(50, int(last_page)+inc,inc):
                    new_url=f'{url}&sr={i}'
                    html=scraper.scrape(new_url)[0]
                    df=IslingtonContentReader(html).create_df()
                    print("df made")
                    dataframes.append(df)
    combined_dfs=pd.concat(dataframes, axis=0, ignore_index=True)
    print((f'csv with title {content_title}.csv will be made'))
    return combined_dfs

        
        


            
    #         inc=50
    #     for i in range(50, int(last_page)+inc, inc):
    #         url_to_scrape=f"{url}&sr={i}"
    #         html=scrape(url_to_scrape, selenium_driver)[0]
    #         df=create_df(html, "islington")
    #         dataframes.append(df)

    # selenium_driver.quit()
    # combined_dfs=pd.concat(dataframes, axis=0, ignore_index=True)
    # combined_dfs.to_csv(f'{content_title}.csv')




