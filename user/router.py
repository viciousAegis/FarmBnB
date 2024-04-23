from flask import Flask, request, jsonify
import json
from pymongo import MongoClient
import bcrypt
import os
from handlers import LengthValidationHandler, AlphanumericValidationHandler, EmailValidationHandler, ValidationException
from bson import ObjectId

class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app = Flask(__name__)
app.json_encoder = MongoJsonEncoder

mongo_uri = "mongodb+srv://admin:admin@database.r0vy6ca.mongodb.net/?retryWrites=true&w=majority&appName=Database"
client = MongoClient(mongo_uri)
db = client['farmbnb']
users = db.user

# Validation handlers setup
length_for_username = LengthValidationHandler(3, 50)
alphanumeric = AlphanumericValidationHandler()
length_for_password = LengthValidationHandler(8, 50)
length_for_email = LengthValidationHandler(3, 50)
email_validator = EmailValidationHandler()

# Setting up validation chains
length_for_username.set_next(alphanumeric)
length_for_password.set_next(None)
length_for_email.set_next(email_validator) 

# Helper function to find a user by email
def find_user_by_email(email):
    return users.find_one({"email": email})



@app.route('/user/login', methods=['POST'])
def login():
    credentials = request.json
    user = find_user_by_email(credentials['email'])
    password_provided = credentials['password'].encode('utf-8')

    # Converting the hashed password from string to bytes if it's not already bytes
    hashed_password_from_db = user['password']
    if isinstance(hashed_password_from_db, str):
        hashed_password_from_db = hashed_password_from_db.encode('utf-8')
    print(user)

    if user and bcrypt.checkpw(password_provided, hashed_password_from_db):
        # Password is correct
        print("Login successful.")
        user.pop('password')
        user.pop('_id')
        return jsonify({"message": "Login successful", "user": user}), 200
    else:
        # Password is incorrect
        print("Login failed.")
        return jsonify({"message": "Invalid credentials"}), 401



@app.route('/user/register', methods=['POST'])
def register():
    user_data = request.json

    # Validate email
    try:
        length_for_email.handle(user_data['email'], "Email")
    except ValidationException as e:
        return jsonify({"message": str(e)}), 400

    # Check if user already exists
    if users.find_one({"email": user_data['email']}):
        return jsonify({"message": "Email already exists"}), 400
    
    if users.find_one({"username": user_data['username']}):
        return jsonify({"message": "User already exists"}), 400

    # Validate username
    try:
        length_for_username.handle(user_data['username'], "Username")
    except ValidationException as e:
        return jsonify({"message": str(e)}), 400

    # Validate password
    try:
        length_for_password.handle(user_data['password'], "Password")
    except ValidationException as e:
        return jsonify({"message": str(e)}), 400

    # Hash password
    hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
    user_data['password'] = hashed_password.decode('utf-8')  # Store decoded hash for compatibility

    # Insert new user into the database
    users.insert_one(user_data)

    # Remove password from user details before returning it
    user_data.pop('password')
    user_data.pop('_id')
    print(user_data)
    return jsonify({"message": "User registered", "user": user_data}), 201



# Profile endpoint
@app.route('/user/profile', methods=['GET'])
def profile():
    email = request.args.get('email')
    print(email)
    user = find_user_by_email(email)
    if user:
        user.pop('password') 
        user.pop('_id')
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404

# List users endpoint
@app.route('/user/list', methods=['GET'])
def list_users():
    user_list = list(users.find({}, {"password": 0}))
    print(user_list)
    for user_detail in user_list:
        user_detail.pop('_id')
    print(user_list)
    return jsonify(user_list), 200

if __name__ == "__main__":
    app.run(port=5002, debug=False)