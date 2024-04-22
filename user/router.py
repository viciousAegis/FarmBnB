from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt
import os

app = Flask(__name__)

# MongoDB setup
# mongo_uri = os.getenv('MONGO_URI', 'your-default-mongodb-uri')
mongo_uri = "mongodb+srv://admin:admin@database.r0vy6ca.mongodb.net/?retryWrites=true&w=majority&appName=Database"
client = MongoClient(mongo_uri)
db = client['farmbnb']
users = db.user

# Helper function to find a user by email
def find_user_by_email(email):
    return users.find_one({"email": email})

# Login endpoint
@app.route('/user/login', methods=['POST'])
def login():
    credentials = request.json
    user = find_user_by_email(credentials['email'])
    if user and bcrypt.checkpw(credentials['password'].encode('utf-8'), user['password']):
        user.pop('password')  # Remove password from user details before returning it
        return jsonify({"message": "Login successful", "user": user}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Registration endpoint
@app.route('/user/register', methods=['POST'])
def register():
    user_data = request.json
    if find_user_by_email(user_data['email']):
        return jsonify({"message": "Email already exists"}), 400
    hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
    user_data['password'] = hashed_password
    users.insert_one(user_data)
    user_data.pop('password')  # Remove password from user details before returning it
    return jsonify({"message": "User registered", "user": user_data}), 201

# Profile endpoint
@app.route('/user/profile', methods=['GET'])
def profile():
    email = request.args.get('email')
    user = find_user_by_email(email)
    if user:
        user.pop('password')  # Remove password from user details before returning it
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404

# List users endpoint
@app.route('/user/list', methods=['GET'])
def list_users():
    user_list = list(users.find({}, {"password": 0}))  # Exclude password field from the result
    return jsonify(user_list), 200

if __name__ == "__main__":
    app.run(port=5002, debug=False)  # Set debug to False for production