import os
import random
import string
from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
from payment_strategy import UpiPaymentStrategy, CardPaymentStrategy
from flask_cors import CORS

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get("MONGO_URI")
if MONGO_URI is None:
    raise ValueError("MONGO_URI environment variable is not set")
try:
    client = MongoClient(MONGO_URI)
    db = client.farmbnb
    user_collection = db.user
    farm_collection = db.farm
    print("Connected to MongoDB")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")


@app.route("/pay/book", methods=["POST"])
def process_payment_and_book():
    user_id = request.json.get("user_id")
    total_price = request.json.get("total_price")
    payment_info = request.json.get("payment_info")
    
    payment_method = request.json.get("payment_method")
    if payment_method == "upi":
        payment_strategy = UpiPaymentStrategy()
    elif payment_method == "card":
        payment_strategy = CardPaymentStrategy()
    else:
        return jsonify({"status": "error", "message": "Invalid payment method"})
    payment_result = payment_strategy.process_payment(user_id, total_price, payment_info)
    if payment_result["status"] == "success":
        user_collection.update_one({"user_id": user_id}, {"$inc": {"wallet_balance": -total_price}})
        return jsonify(payment_result)
    else:
        return jsonify({"status": "error", "message": f"Payment using {payment_method} failed"})


@app.route('/pay/wallet', methods=['POST'])
def pay_using_wallet():
    user_id = request.json.get("user_id")
    total_price = int(request.json.get("total_price"))
    user = user_collection.find_one({"user_id": user_id})
    if user is None:
        return jsonify({"status": "error", "message": "User not found"})
    if user["wallet_balance"] < total_price:
        return jsonify({"status": "error", "message": "Insufficient balance"})
    user_collection.update_one({"user_id": user_id}, {"$inc": {"wallet_balance": -total_price}})
    return jsonify({"status": "success", "message": "Payment successful using wallet"})

@app.route('/health')
def health_check():
    return "OK"

if __name__ == "__main__":
    app.run(debug=False, port=5002)
