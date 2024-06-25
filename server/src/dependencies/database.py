import pymongo

class Database():
    def __init__(self, mongo_db_uri, db):
        self.client = pymongo.MongoClient(mongo_db_uri)
        self.db = self.client[db]
    
    def close(self):
        self.client.close()
    

    def save_many(self, collection_name, items, update=None):
        collection=self.db[collection_name]
        current_links=collection.distinct("category_link")
        print(current_links, "current links")
        for item in items:
            if update is not None:
                item.update(update)
            if item["category_link"] not in current_links:
                    collection.find_one_and_replace({"category_name":item["category_name"]}, item, upsert=True)
        print(f"{len(items)} entries saved to {collection_name}")

    def get_key_values(self, collection_name, key1, *additional_keys):
        collection = self.db[collection_name]
        # Create the projection dictionary with the required key
        projection = {key1: 1, "_id": 0}
        # Add any additional keys to the projection
        for key in additional_keys:
            projection[key] = 1
        # Fetch the documents with the specified keys
        keys = collection.find({}, projection)
        return list(keys)
         

    
