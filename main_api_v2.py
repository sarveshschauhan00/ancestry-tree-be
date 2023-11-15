from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app, resources={r"/lookup": {"origins": "*"}})  # Allow all origins for the /lookup route

# client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string

# # Select the database and collection
# db = client['mydb']  # Replace with your database name
# collection = db['mycollection']  # Replace with your collection name

# MongoDB connection settings
host = "localhost"  # Replace with your MongoDB server's hostname or IP address
port = 27017        # Default MongoDB port
database_name = "family_tree"
persons_collection_name = "persons"
relationships_collection_name = "relationships"

# Connect to MongoDB
client = MongoClient(host, port)
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


def print_family_tree(person, level=0, ls=[], mid='', fid=''):
    # Print a family tree for a person and their descendants
    indent = "    " * level

    # Get the person's spouse (husband or wife)
    spouse = get_spouse(person['_id'])
    if spouse:
        print(f"{indent} - {person['name']} || {spouse['name']}")
        # print(f"{indent} - {person['name']} ({person['_id']}) || Spouse: {spouse['name']} ({spouse['_id']})")
        # { id: 3, mid: 1, fid: 2, name: "Peter Stevens", gender: "male", img: "https://cdn.balkan.app/shared/m10/2.jpg" },
        if mid or fid:
            if { "id": str(person["_id"]), "pids":[str(spouse["_id"])], "mid": mid, "fid": fid, "name": person["name"], "gender": person["gender"], "img": "" } not in ls: 
                ls.append({ "id": str(person["_id"]), "pids":[str(spouse["_id"])], "mid": mid, "fid": fid, "name": person["name"], "gender": person["gender"], "img": "" })
        else:
            if { "id": str(person["_id"]), "pids":[str(spouse["_id"])], "name": person["name"], "gender": person["gender"], "img": "" } not in ls: 
                ls.append({ "id": str(person["_id"]), "pids":[str(spouse["_id"])], "name": person["name"], "gender": person["gender"], "img": "" })
        if { "id": str(spouse["_id"]), "pids":[str(person["_id"])], "name": spouse["name"], "gender": spouse["gender"], "img": "" } not in ls: 
            ls.append({ "id": str(spouse["_id"]), "pids":[str(person["_id"])], "name": spouse["name"], "gender": spouse["gender"], "img": "" })
    else:
        print(f"{indent} - {person['name']}")
        # print(f"{indent} - {person['name']} ({person['_id']})")
        if mid or fid:
            if { "id": str(person["_id"]), "mid": mid, "fid": fid, "name": person["name"], "gender": person["gender"], "img": "" } not in ls: 
                ls.append({ "id": str(person["_id"]), "mid": mid, "fid": fid, "name": person["name"], "gender": person["gender"], "img": "" })
        else:
            if { "id": str(person["_id"]), "name": person["name"], "gender": person["gender"], "img": "" } not in ls: 
                ls.append({ "id": str(person["_id"]), "name": person["name"], "gender": person["gender"], "img": "" })

    childrens = get_children(person["_id"])
    
    # print("spouse: ", spouse)
    # print("childrens: ", childrens)

    for child in childrens:
        if person["gender"] == "male":
            print_family_tree(child, level + 1, ls, str(person["_id"]), str(spouse["_id"]))
        else:
            print_family_tree(child, level + 1, ls, str(person["_id"]), str(spouse["_id"]))

    return ls

def getRelations():
    pass

# @app.route('/add', methods=['POST'])
# def add_document():
#     data = request.json
#     persons_collection.insert_one(data)
#     return 'Document added successfully', 201

@app.route('/lookup', methods=['POST'])
def lookup_document():
    data = request.json
    person = persons_collection.find_one({"_id": ObjectId(data['id'])})
    if person:
        print("Family Tree:")
        d = print_family_tree(person)
        # print(d)
        return jsonify(d)
    else:
        return 'Person not found', 404

@app.route('/delete/<id>', methods=['DELETE'])
def delete_document(id):
    result = persons_collection.delete_one({'_id': id})
    if result.deleted_count == 1:
        return 'Document deleted successfully', 204
    return 'Document not found', 404


@app.route('/update/<id>', methods=['PUT'])
def update_document(id):
    data = request.json
    result = persons_collection.update_one({'_id': id}, {'$set': data})
    if result.modified_count == 1:
        return 'Document updated successfully', 200
    return 'Document not found', 404


if __name__ == '__main__':
    app.run(debug=True)



