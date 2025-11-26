from pymongo import MongoClient

client = MongoClient()

database = client.mydatabase

user_collection = database["users"]

# user_collection.insert_one({"name": "test user", "email": 'test@email.com'})
