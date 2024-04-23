from flask import Flask, request
import os
from dotenv import load_dotenv
from pymongo import MongoClient

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

@app.route("/farm/list", methods=["GET", "POST"])
def list_farms():
    print("List of farms")
    print(request.json)
    return {"message": "List of farms"}

if __name__ == "__main__":
    app.run(port=5001) # port for the farm server (5001)