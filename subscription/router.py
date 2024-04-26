from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_cors import CORS
from subscriptionManager import SubscriptionManager

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
    farm_collection = db.farm
    userfarm_collection = db.user_farm
    subscription_collection = db.subscriptions
    print("Connected to MongoDB")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

SubscriptionManager = SubscriptionManager(subscription_collection)

@app.route("/subscription/health", methods=["GET"])
def health_check():
    return "OK"

@app.route("/subscription/getsubscribers", methods=["GET"])
def get_subscribers():
    farm_id = request.args.get("farm_id")
    try:
        subscribers = SubscriptionManager.getSubscriptionsByFarm(farm_id)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    # add status code
    return jsonify({"status": "success"}, subscribers)

@app.route("/subscription/subscribe", methods=["POST"])
def subscribe():
    farm_id = request.json.get("farm_id")
    user_email = request.json.get("user_email")
    try:
        SubscriptionManager.addSubscription(farm_id, user_email)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "success", "message": "Subscribed successfully"})

@app.route("/subscription/unsubscribe", methods=["POST"])
def unsubscribe():
    farm_id = request.json.get("farm_id")
    user_email = request.json.get("user_email")
    try:
        SubscriptionManager.removeSubscription(farm_id, user_email)
    except Exception as e:
        return jsonify({"status": "success", "message": str(e)})
    return jsonify({"status": "error", "message": "Unsubscribed successfully"})

@app.route("/subscription/notify", methods=["POST"])
def notify():
    farm_id = request.json.get("farm_id")
    message = request.json.get("message")

    try:
        SubscriptionManager.notifySubscribers(farm_id, message)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "success","message": "Notification sent successfully"})

@app.route("/subscription/getsubscriptions", methods=["GET"])
def get_subscriptions():
    print("get subscriptions")
    user_id = request.args.get("user_id")
    try:
        subscriptions = SubscriptionManager.getSubscriptionsByUser(user_id)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "success"}, subscriptions)

if __name__ == "__main__":
    app.run(port=5003)
