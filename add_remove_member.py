import pymongo
from bson import ObjectId

# MongoDB's connection settings
host = "localhost"  # Replace with the MongoDB server hostname or IP address
port = 27017        # Default MongoDB port
database_name = "family_tree"
persons_collection_name = "persons"
relationships_collection_name = "relationships"

# Connect to MongoDB
client = pymongo.MongoClient(host, port)
db = client[database_name]
persons_collection = db[persons_collection_name]
relationships_collection = db[relationships_collection_name]

########################################################
# # Drop the "persons" collection
# db.drop_collection(persons_collection_name)
#
# # Drop the "relationships" collection
# db.drop_collection(relationships_collection_name)
########################################################

def add_person(name, gender):
    # Add a person to the persons collection
    person_data = {
        "name": name,
        "gender": gender,
    }
    result = persons_collection.insert_one(person_data)
    return result.inserted_id


def remove_person(person_id):
    # Remove a person from the persons collection and related relationships
    result = persons_collection.delete_one({"_id": ObjectId(person_id)})
    relationships_collection.delete_many({"$or": [{"person1_id": ObjectId(person_id)}, {"person2_id": ObjectId(person_id)}]})
    return result.deleted_count


def add_relationship(person1_id, person2_id, relationship_type):
    relations = {
        "parent": "child",
        "child": "parent",
        "husband": "wife",
        "wife": "husband"
    }
    # Add a relationship between two persons to the relationships collection
    relationship_data = {
        "person1_id": ObjectId(person1_id),
        "person2_id": ObjectId(person2_id),
        "relationship_type": relationship_type
    }
    reversed_relationship_data = {
        "person1_id": ObjectId(person2_id),
        "person2_id": ObjectId(person1_id),
        "relationship_type": relations[relationship_type]
    }

    result = relationships_collection.insert_one(relationship_data)
    relationships_collection.insert_one(reversed_relationship_data)
    return result.inserted_id


def main():
    while True:
        print("\nFamily Tree Management Menu:")
        print("1. Add Person")
        print("2. Remove Person")
        print("3. Add Relationship")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter person's full name: ")
            gender = input("Enter person's gender: ")
            # middle_name = input("(Optional)Enter person's middle name: ")
            # last_name = input("Enter person's last name: ")
            # birthdate = input("Enter person's birthdate: ")
            # other_info = {}
            # Add any additional information here
            person_id = add_person(name, gender)
            print(f"Person added with ID: {person_id}")
        
        elif choice == "2":
            person_id = input("Enter person's ID to remove: ")
            deleted_count = remove_person(person_id)
            print(f"Deleted {deleted_count} person(s) and related relationships.")
        
        elif choice == "3":
            person1_id = input("Enter person1's ID: ")
            person2_id = input("Enter person2's ID: ")

            # Use find_one to check if the ObjectId exists
            document1 = persons_collection.find_one({'_id': ObjectId(person1_id)})
            document2 = persons_collection.find_one({'_id': ObjectId(person2_id)})
            if document1 and document2:
                # print("ObjectId exists in the collection.")
                relationship_type = input("Enter relationship type: ")
                relationship_id = add_relationship(person1_id, person2_id, relationship_type)
                print("Relationship added")
                # print(f"Relationship added with ID: {relationship_id}")
            else:
                print("person1 or person2 does not exist in the collection.")
        
        elif choice == "4":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
