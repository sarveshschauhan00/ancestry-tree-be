import pymongo

# MongoDB connection settings
host = "localhost"  # Use the IP or hostname where your MongoDB container is running
port = 27017        # Default MongoDB port
database_name = "mydb"
collection_name = "mycollection"

# Connect to MongoDB
client = pymongo.MongoClient(host, port)

# Access a specific database
db = client[database_name]

# Access a specific collection
collection = db[collection_name]

# Insert a document into the collection
data_to_insert = {"name": "John", "age": 30}
inserted_document = collection.insert_one(data_to_insert)
print(f"Inserted document ID: {inserted_document.inserted_id}")

# Query data from the collection
query = {"name": "John"}
result = collection.find_one(query)
print(result)

# Close the MongoDB connection
client.close()
