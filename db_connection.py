import os

import pymongo

# url = 'mongodb://localhost:27017/'
# url = 'mongodb://app-db-mongo-srv:27017/appdb'
url = os.environ.get('MONGO_URL')

client = pymongo.MongoClient(url)

db = client['tracking_system']
