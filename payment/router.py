import os
from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

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



@app.route("/pay/upi", methods=["GET"])
def upi_payment():
    return jsonify({"message": "UPI payment successful"})

if __name__ == "__main__":
    app.run(debug=False, port=5002)
