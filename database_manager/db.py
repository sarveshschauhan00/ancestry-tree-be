from pymongo import MongoClient


def create_database(database_name):
    # Create a MongoClient to connect to the MongoDB server running on localhost
    client = MongoClient('localhost', 27017)

    # Create a new database name
    db = client[database_name]

    # List all available databases on the MongoDB server
    print(client.list_database_names())

    # Close the MongoDB connection
    client.close()

def remove_database(database_name):
    # Create a MongoClient to connect to the MongoDB server
    client = MongoClient('localhost', 27017)  # Replace with your MongoDB server address and port

    # Specify the name of the database you want to delete
    database_name = database_name  # Replace with the name of your database

    # Use the drop_database() method to delete the database
    client.drop_database(database_name)

    # Verify that the database has been deleted by listing all available databases
    print(client.list_database_names())

    # Close the MongoDB connection
    client.close()

def create_collectiion(database_name, collection_name):
    # Create a MongoClient to connect to the MongoDB server running on localhost
    client = MongoClient('localhost', 27017)

    # Select a database
    db = client[database_name]

    # Create a collection named 'mycollection' and insert a document into it
    collection = db[collection_name]

    # Insert a document into the collection
    data_to_insert = {"name": "John", "age": 30}
    inserted_document = collection.insert_one(data_to_insert)
    print(f"Inserted document ID: {inserted_document.inserted_id}")

    # List collections in the current database
    print(db.list_collection_names())

    # Close the MongoDB connection
    client.close()

def list_databases():
    # Create a MongoClient to connect to the MongoDB server running on localhost
    client = MongoClient('localhost', 27017)

    # List all available databases on the MongoDB server
    ls = client.list_database_names()

    # Close the MongoDB connection
    client.close()
    return ls

def list_collections(database_name):
    # Create a MongoClient to connect to the MongoDB server running on localhost
    client = MongoClient('localhost', 27017)

    # Select a database
    db = client[database_name]

    # List collections in the current database
    ls = db.list_collection_names()

    # Close the MongoDB connection
    client.close()
    return ls

