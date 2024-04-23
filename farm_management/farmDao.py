from dotenv import load_dotenv
from flask import jsonify
from bson.objectid import ObjectId


class FarmDao():
    def __init__(self, db):
        self.db = db
        self.farm_collection = db.farm
    
    def list_farms(self):
        try:
            all_users = list(self.farm_collection.find())
            for user in all_users:
                user["_id"] = str(user["_id"])
            return jsonify(all_users)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def get_farm_by_id(self, id):
        try:
            farm = self.farm_collection.find_one({"_id": ObjectId(id)})
            if farm is None:
                return jsonify({"error": "Farm not found"}), 404
            
            farm["_id"] = str(farm["_id"])
            return jsonify(farm)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
