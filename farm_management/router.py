from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI")
if MONGO_URI is None:
    raise ValueError("MONGO_URI environment variable is not set")
try:
    client = MongoClient(MONGO_URI)
    db = client.farmbnb
    farm_collection = db.farm
    print("Connected to MongoDB")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

'''
this is the health check endpoint for the farm server.
this is used to check if the farm server is running.
'''
@app.route('/health')
def health_check():
    return 'OK'

@app.route("/farm/list", methods=["GET", "POST"])
def list_farms():
    print("List of farms")
    print(request.json)
    try:
        all_users = list(farm_collection.find())
        for user in all_users:
            user["_id"] = str(user["_id"])
        return jsonify(all_users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/farm/<id>", methods=["GET"])
def get_farm(id):
    print("Get farm")
    try:
        farm = farm_collection.find_one({"_id": ObjectId(id)})
        if farm is None:
            return jsonify({"error": "Farm not found"}), 404
        
        farm["_id"] = str(farm["_id"])
        return jsonify(farm)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001) # port for the farm server (5001)