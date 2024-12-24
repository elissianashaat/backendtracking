import os

import pymongo

url = os.environ.get('MONGO_URL')

client = pymongo.MongoClient(url)

db = client['tracking_system']
