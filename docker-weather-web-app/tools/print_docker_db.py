import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pprint import pprint

def print_mongodb_db():
    """
    prints data in mongodb volume
    """
    load_dotenv()
    mongo_uri = os.getenv('MONGO_LOCAL_URI')
    client = MongoClient(mongo_uri)
    db = client['weather_db']
    collection = db['daily_summaries']

    for data in collection.find():
        filtered_data = {}
        for key in data:
            if key != '_id':
                filtered_data[key] = data[key]
        pprint(filtered_data)
        print("\n")

if __name__ == "__main__":
    print_mongodb_db()
