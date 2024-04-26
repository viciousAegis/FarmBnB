from pymongo import MongoClient

class PaymentDao:
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.farmbnb
        self.user_collection = self.db.user

    def get_wallet_balance(self, user_id):
        user = self.user_collection.find_one({"id": user_id})
        return user.get("wallet_balance", 0)

    def increase_wallet_balance(self, user_id, amount):
        self.user_collection.update_one({"id": user_id}, {"$inc": {"wallet_balance": float(amount)}})

    def decrease_wallet_balance(self, user_id, amount):
        print("decreasing wallet balance")
        # print(-float(amount)
        self.user_collection.update_one({"id": user_id}, {"$inc": {"wallet_balance": float(amount)}})