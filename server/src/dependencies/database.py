import pymongo
from urllib.parse import urlparse, parse_qs, urlencode
import re

class Database():
    def __init__(self, mongo_db_uri, db):
        self.client = pymongo.MongoClient(mongo_db_uri)
        self.db = self.client[db]
    
    def close(self):
        self.client.close()

    def get_key_values(self, collection_name, key1, *additional_keys, exclude_field_name=False):
        if exclude_field_name and additional_keys:
            raise ValueError("Cannot exclude field names when returning multiple key values")
        collection = self.db[collection_name]
        projection = {key1: 1, "_id": 0}
        for key in additional_keys:
            projection[key] = 1
        keys = collection.find({}, projection)
        key_value_list=list(keys)
        if exclude_field_name:
            key_value_list=[item[key1] for item in key_value_list]
        return key_value_list
    
class LocalDirectoryDatabase(Database):
    def save_many(self, collection_name, distinct_key, items, update=None):
        collection=self.db[collection_name]
        category_type=distinct_key.split("_")[0]
        current_links=collection.distinct(distinct_key)
        for item in items:
            if update is not None:
                item.update(update)
            if item[distinct_key] not in current_links:
                    collection.find_one_and_replace({f"{category_type}_name":item[f"{category_type}_name"]}, item, upsert=True)
        print(f"{len(items)} entries saved to {collection_name}")

    def get_main_regional_categories(self, region):
        collection=self.db["main_categories"]
        categories=collection.find({"region":region}, projection={"_id":0})
        return list(categories)

    def get_regional_subcategories(self,request_url, region):
        parsed_url = urlparse(request_url)
        # Extract the query parameters
        query_params = parse_qs(parsed_url.query)
        
        # Process parameters that include 'channel' in their names
        processed_params = {}
        for key, value in query_params.items():
            if 'channel' in key:
                if value:
                    processed_params[key] = value[0].split('-')[0]
        if region=="camden":
            filter=urlencode(processed_params)+"-"
        elif region=="islington":
            filter=list(processed_params.keys())[0]
        regex_pattern = re.compile(filter, re.IGNORECASE)
        collection=self.db["subcategories"]
        results = collection.find( {"subcategory_link": {'$regex': regex_pattern}}, projection={"_id":0})
        results_list = list(results)
        return results_list
         

class SignpostingDatabase(Database):
    def get_items(self):
        pass