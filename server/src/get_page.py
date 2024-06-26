
from dependencies.database import Database
from dependencies.categories import Categories

from dotenv import load_dotenv
import os
import json
load_dotenv()
json_file="subcategories.json"
content_json_file="subcategory_content.json"
mongo_db_uri=os.environ.get("MONGODB_URI")

regions=["camden", "islington"]
db=Database(mongo_db_uri, "directory-contents")
main_category_urls=db.get_key_values("main_categories", "category_link", "region")
sub_category_urls=db.get_key_values("subcategories", "subcategory_link", "region")
test_link={'category_link': 'https://findyour.islington.gov.uk/kb5/islington/directory/health.page?healthchannelnew=0', 'region': 'islington'}

def update_main_categories(regions):
   categories=[]
   for region in regions:
      main_categories=Categories().get_main_categories(region)
      main_categories.update({"region": region})
      categories.extend(main_categories)
   db.save_many("main_categories", "category_link", categories)


def update_subcategories(urls, main_category_json_file_path):
   all_subcategories=[]
   for url in urls:
      subcategories= Categories().get_subcategories(url["category_link"], url["region"])
      all_subcategories.extend(subcategories)  # Add the new subcategories to the list
   with open(json_file, 'w') as f:
      json.dump(main_category_json_file_path, f, indent=4)
   try:
    # Read and parse the JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Loop through the contents
    for item in data:
        subcategory_link = item.get("subcategory_link")
        if "camden" in subcategory_link:
            item.update({"region": "camden"})
        elif "islington" in subcategory_link:
            item.update({"region": "islington"})
    db.save_many("subcategories", "subcategory_link", data) 
   except FileNotFoundError:
      print(f"The file {json_file} does not exist.")
   except json.JSONDecodeError:
      print(f"Error decoding JSON from the file {json_file}.")

def update_page_content(sub_category_urls):
   all_content=[]
   for obj in sub_category_urls:
      scraped_data=Categories().get_subcategory_content(obj["subcategory_link"], obj["region"])
      all_content.append(scraped_data)

   with open(content_json_file, "w", encoding='utf-8') as file:
        json.dump(all_content, file, indent=4)
      

update_page_content(sub_category_urls)
