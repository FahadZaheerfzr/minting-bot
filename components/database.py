from pymongo import MongoClient

client = MongoClient("mongodb+srv://mintbot:passwordmint@cluster0.2l61ojr.mongodb.net/?retryWrites=true&w=majority")
DB = client.mintster

print(DB)