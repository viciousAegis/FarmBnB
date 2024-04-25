from pymongo import MongoClient

class PaymentDao:
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.farmbnb
        self.user_collection = self.db.user

    def update_wallet_balance(self, user_id, amount):
        self.user_collection.update_one({"user_id": user_id}, {"$inc": {"wallet_balance": amount}})
