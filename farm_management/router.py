from flask import Flask, request, jsonify
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from farm import Farm
from farmDao import FarmDao
import datetime
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

def insert_farm():
    test_farm = Farm("3", "Farm3", "Farm3 description", "Farm3 location", "Farm3 area", 12, "Farm3 owner", "Farm3 contact", "Farm3 farm_type", 4.4)
    farm_collection.insert_one(test_farm.__dict__)


@app.route("/farm/list", methods=["GET"])
def list_farms():
    print("List of farms")
    # print(request.json)
    
    farmDao = FarmDao(db)
    
    farmlist = farmDao.list_farms()

    # print(farmlist)

    return farmlist

    
@app.route("/farm/<id>", methods=["GET"])
def get_farm(id):
    print("Get farm")
    
    farmDao = FarmDao(db)

    return farmDao.get_farm_by_id(id)


if __name__ == "__main__":
    app.run(port=5003) # port for the farm server (5001)
