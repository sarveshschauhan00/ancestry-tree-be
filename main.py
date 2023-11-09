import pymongo
from bson import ObjectId
from database_manager import db


db_name = "AncestryBook"
collection_name = "FamilyTree"

db.create_collectiion(database_name=db_name, collection_name=collection_name)

# print(db.list_collections(db_name))




