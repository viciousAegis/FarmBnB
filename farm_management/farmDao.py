from dotenv import load_dotenv
from flask import jsonify
from bson.objectid import ObjectId


class FarmDao():
    def __init__(self, db):
        self.db = db
        self.farm_collection = db.farm
    
    def list_farms(self):
        try:
            all_farms = list(self.farm_collection.find())
            for farms in all_farms:
                farms["_id"] = str(farms["_id"])
            return jsonify(all_farms), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def get_farm_by_id(self, id):
        try:
            farm = self.farm_collection.find_one({"farm_id": id})
            if farm is None:
                return jsonify({"error": "Farm not found"}), 404
            
            farm["_id"] = str(farm["_id"])
            return jsonify(farm), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def get_farm_by_farmid(self, farm_id):
        try:
            farm = self.farm_collection.find_one({"farm_id": farm_id})
            if farm is None:
                return jsonify({"error": "Farm not found"}), 404
            
            farm["_id"] = str(farm["_id"])
            return jsonify(farm), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def rate_farm(self, farm_id, rating):
        try:
            farm = self.farm_collection.find_one({"farm_id": farm_id})
            if farm is None:
                return jsonify({"error": "Farm not found"}), 404
            
            print(farm)

            
            # self.farm_collection.update_one({"farm_id": ObjectId(id)}, {"$set": {"rating": rating}}) 
            self.farm_collection.update_one({"farm_id": farm_id}, {"$push": {"rating": rating}})

            print(farm['rating'])

            farm['rating'].append(rating)

            print(farm['rating'])

            avg_rating = sum(farm['rating']) / len(farm['rating'])

            print(avg_rating)

            self.farm_collection.update_one({"farm_id": farm_id}, {"$set": {"avg_rating": avg_rating}})

            return jsonify({"message": "Farm rating updated successfully"}), 200
        except Exception as e:
            print("Exception",e)
            return jsonify({"error": str(e)}), 500