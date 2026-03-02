from pymongo import MongoClient
from config.settings import helper

client = MongoClient(helper.mongodb_connection_string)

# print(client.admin.command({"ping":1}))
# database name
db = client['document_ai']