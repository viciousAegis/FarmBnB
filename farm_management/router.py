from flask import Flask, request, jsonify
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from farm import Farm
from farmDao import FarmDao
from userFarm import UserFarm
from userFarmDao import UserFarmDao
from datetime import datetime
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
    userfarm_collection = db.user_farm
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

def insert_userfarm():
    test_userfarm = UserFarm("2", "1", "2024-04-21", "2024-04-23", 40, 3)
    userfarm_collection.insert_one(test_userfarm.__dict__)


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

@app.route("/userfarm/list", methods=["GET"])
def list_userfarms():
    print("List of user farms")
    # print(request.json)
    insert_userfarm()
    
    userfarmDao = UserFarmDao(db)
    
    userfarmlist = userfarmDao.list_userfarms()

    # print(userfarmlist)

    return userfarmlist

@app.route("/farm/check_availability", methods=["GET"])
def check_availability():
    start_date_str = request.json["start_date"]
    end_date_str = request.json["end_date"]
    farm_id = request.json["farm_id"]

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()


    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400
    
    if not farm_id:
        return jsonify({"error": "farm_id is required"}), 400
    
    userFarmDao = UserFarmDao(db)
    userfarms = userFarmDao.get_userfarm_by_farmid(farm_id).get_json()

    for userfarm in userfarms:
        booked_start_date = datetime.strptime(userfarm["start_date"], "%Y-%m-%d").date()
        booked_end_date = datetime.strptime(userfarm["end_date"], "%Y-%m-%d").date()

        if (start_date < booked_start_date and end_date >= booked_start_date) or (start_date >= booked_start_date and start_date <= booked_end_date):
            return jsonify({"available": False})
        
    return jsonify({"available": True})
    

if __name__ == "__main__":
    app.run(port=5001) # port for the farm server (5001)
