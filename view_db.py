import pymongo

# MongoDB connection settings
host = "localhost"  # Replace with your MongoDB server's hostname or IP address
port = 27017        # Default MongoDB port
# database_name = "mydb"  # Replace with your database name
database_name = "family_tree"

# Connect to MongoDB
client = pymongo.MongoClient(host, port)
db = client[database_name]

# Get a list of all collection names in the database
collection_names = db.list_collection_names()

# Print the list of collection names
for collection_name in collection_names:
    print(f"Collection Name: {collection_name}")
    # Access the collection
    collection = db[collection_name]
    # Find and print all documents in the collection
    for document in collection.find():
        print(document)
