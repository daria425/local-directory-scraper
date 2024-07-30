from dependencies.database import LocalDirectoryDatabase
from dependencies.helpers import replace_url
from dependencies.make_csv import make_category_csv
import os
from dependencies.autotagging import classify_location
from dotenv import load_dotenv
load_dotenv()
mongo_db_uri=os.getenv("LOCAL_DIRECTORY_DB_URI")
directory_db=LocalDirectoryDatabase(mongo_db_uri, "directory-contents")


# sample_url="https://cindex.camden.gov.uk/kb5/camden/cd/results.action?communitychannel=1-7"
# region="camden"
# url=replace_url(sample_url)
# df=make_category_csv(url, region, use_local_classifier=True)
# df.to_csv("test.csv")

text="National organisation with some London-wide projects working with and for families affected by drugs and alcohol."
r=classify_location(text, True)
print(r)