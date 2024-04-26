from dotenv import load_dotenv
from flask import jsonify
from bson.objectid import ObjectId



class UserFarmDao():
    def __init__(self, db):
        self.db = db
        self.userfarm_collection = db.user_farm
    
    def insert_userfarm(self, userFarm):
        try:
            self.userfarm_collection.insert_one(userFarm.__dict__)
            return jsonify({"message": "UserFarm inserted successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def list_userfarms(self):
        try:
            all_userfarms = list(self.userfarm_collection.find())
            for userfarm in all_userfarms:
                userfarm["_id"] = str(userfarm["_id"])
            return jsonify(all_userfarms), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def get_userfarm_by_userid(self, user_id):
        try:
            userfarms = list(self.userfarm_collection.find({"user_id": user_id}))
            for userfarm in userfarms:
                userfarm["_id"] = str(userfarm["_id"])
            return jsonify(userfarms), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def get_userfarm_by_farmid(self, farm_id):
        try:
            userfarms = list(self.userfarm_collection.find({"farm_id": farm_id}))
            for userfarm in userfarms:
                userfarm["_id"] = str(userfarm["_id"])
            return jsonify(userfarms), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def get_userfarm_by_user_farm_id(self, user_id, farm_id):
        try:
            userfarms = list(self.userfarm_collection.find({"user_id": user_id, "farm_id": farm_id}))
            for userfarm in userfarms:
                userfarm["_id"] = str(userfarm["_id"])
            return jsonify(userfarms), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def rate_userfarm(self, id, user_id, farm_id, rating):
        try:

            # print("id", id)
            print("ObjectId(id)", ObjectId(id))

            # a = self.userfarm_collection.find_one({"_id": id})
            # print("a", a)

            b = self.userfarm_collection.find({"_id": ObjectId(id)})
            print("b", b)


            result = self.userfarm_collection.update_one({"_id": ObjectId(id)}, {"$set": {"rating": rating}})
            print(result)

            if result.modified_count == 0:
                return jsonify({"error": "UserFarm not found"}), 404
            return jsonify({"message": "UserFarm rated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
