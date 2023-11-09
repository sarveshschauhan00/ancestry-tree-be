import pymongo
from bson import ObjectId


# MongoDB connection settings
host = "localhost"  # Replace with your MongoDB server's hostname or IP address
port = 27017        # Default MongoDB port
database_name = "family_tree"
persons_collection_name = "persons"
relationships_collection_name = "relationships"

# Connect to MongoDB
client = pymongo.MongoClient(host, port)
db = client[database_name]
persons_collection = db[persons_collection_name]
relationships_collection = db[relationships_collection_name]


def get_children(person_id):
    # Retrieve the children of a person from the relationships collection
    children = []
    relationships = relationships_collection.find({"person1_id": person_id, "relationship_type": {"$in": ["child"]}})
    for relationship in relationships:
        child = persons_collection.find_one({"_id": relationship["person2_id"]})
        if child:
            children.append(child)
    return children


def get_spouse(person_id):
    # Find the spouse of a person in the relationships collection
    # You may need to adapt this query depending on your data structure
    query = {
        "$or": [
            {"person1_id": ObjectId(person_id), "relationship_type": "husband"},
            {"person1_id": ObjectId(person_id), "relationship_type": "wife"},
            {"person2_id": ObjectId(person_id), "relationship_type": "husband"},
            {"person2_id": ObjectId(person_id), "relationship_type": "wife"}
        ]
    }
    spouse_relation = relationships_collection.find_one(query)

    if spouse_relation:
        spouse_id = spouse_relation["person1_id"] if spouse_relation["person2_id"] == ObjectId(person_id) else spouse_relation["person2_id"]
        spouse = persons_collection.find_one({"_id": spouse_id})
        return spouse

    return None


def print_family_tree(person, level=0, tree={}):
    # Print a family tree for a person and their descendants
    indent = "    " * level

    # Get the person's spouse (husband or wife)
    spouse = get_spouse(person['_id'])
    if spouse:
        print(f"{indent} - {person['name']} || {spouse['name']}")
        # print(f"{indent} - {person['name']} ({person['_id']}) || Spouse: {spouse['name']} ({spouse['_id']})")
    else:
        print(f"{indent} - {person['name']}")
        # print(f"{indent} - {person['name']} ({person['_id']})")

    children = get_children(person["_id"])
    tree[person['name']] = {}
    for child in children:
        tree[person['name']][child['name']] = {}
        print_family_tree(child, level + 1, tree[person['name']])
    return tree


def main():
    person_id = input("Enter the person's ID to view their family tree: ")
    person = persons_collection.find_one({"_id": ObjectId(person_id)})
    if person:
        print("Family Tree:")
        d = print_family_tree(person)
        print(d)
    else:
        print("Person not found.")


if __name__ == "__main__":
    main()
