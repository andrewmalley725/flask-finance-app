# db.py
from pymongo.mongo_client import MongoClient
import certifi
import creds

uri = creds.MONGO_URI
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client['finance-app']
users = db.user
