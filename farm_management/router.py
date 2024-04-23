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

# def insert_farm():
#     test_farm = Farm("1", "Farm1", "Farm1 description", "Farm1 location", "Farm1 area", 20, "Farm1 owner", "01-01-2024", "01-02-2024", "Farm1 contact", "Farm1 farm_type", 3.0)
#     farm_collection.insert_one(test_farm.__dict__)


@app.route("/farm/list", methods=["GET", "POST"])
def list_farms():
    print("List of farms")
    print(request.json)
    
    farmDao = FarmDao(db)
    
    return farmDao.list_farms()

    
@app.route("/farm/<id>", methods=["GET"])
def get_farm(id):
    print("Get farm")
    
    farmDao = FarmDao(db)

    return farmDao.get_farm_by_id(id)

if __name__ == "__main__":
    app.run(port=5001) # port for the farm server (5001)