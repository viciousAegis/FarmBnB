from flask import Flask, request, jsonify
import json
from pymongo import MongoClient
import bcrypt
import os

app = Flask(__name__)

mongo_uri = "mongodb+srv://admin:admin@database.r0vy6ca.mongodb.net/?retryWrites=true&w=majority&appName=Database"
client = MongoClient(mongo_uri)
db = client['farmbnb']


@app.route('/sub/list', methods=['GET'])
def list_subscriptions():
    user_id = request.args.get('user_id')
    subscriptions = db.subscriptions.find({"user_id": user_id})
    return jsonify(list(subscriptions))

@app.route('/sub/subscribe', methods=['POST'])
def subscribe():
    user_id = request.json.get('user_id')
    service_id = request.json.get('service_id')
    if not db.services.find_one({"_id": service_id}):
        return jsonify({"error": "Service not found"}), 404
    subscription = {
        "user_id": user_id,
        "service_id": service_id
    }
    db.subscriptions.insert_one(subscription)
    return jsonify({"message": "Subscribed successfully"}), 201

@app.route('/sub/unsubscribe', methods=['POST'])
def unsubscribe():
    user_id = request.json.get('user_id')
    service_id = request.json.get('service_id')
    db.subscriptions.delete_one({"user_id": user_id, "service_id": service_id})
    return jsonify({"message": "Unsubscribed successfully"})

@app.route('/sub/add', methods=['POST'])
def add_service():
    service = request.json
    db.services.insert_one(service)
    return jsonify({"message": "Service added successfully"}), 201

@app.route('/sub/delete', methods=['POST'])
def delete_service():
    service_id = request.json.get('service_id')
    db.services.delete_one({"_id": service_id})
    db.subscriptions.delete_many({"service_id": service_id})
    return jsonify({"message": "Service deleted successfully"})

if __name__ == "__main__":
    app.run(port=5001)  # port for the farm server (5001)