
from dependencies.database import Database
from dependencies.categories import Categories
from dependencies.helpers import replace_url
from dotenv import load_dotenv
import os
load_dotenv()
mongo_db_uri=os.environ.get("MONGODB_URI")

regions=["camden", "islington"]
urls=Database(mongo_db_uri, "directory-contents").get_key_values("main_categories", "category_link", "region")

 
for url in urls:
   link= Categories().get_subcategories(url["category_link"], url["region"])
   




