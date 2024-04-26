from datetime import datetime
import os
import bcrypt
from flask import Flask, jsonify, request
import subprocess
from pymongo import MongoClient
import requests
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv

from farm_management.farm import Farm
from farm_management.farmDao import FarmDao
from farm_management.userFarm import UserFarm
from farm_management.userFarmDao import UserFarmDao
from payment.payment import Payment
from payment.paymentDao import PaymentDao
from payment.payment_strategy import CardPaymentStrategy, UpiPaymentStrategy
from subscription.subscriptionManager import SubscriptionManager
from user.handlers import (
    AlphanumericValidationHandler,
    EmailValidationHandler,
    LengthValidationHandler,
    ValidationException,
)
from user.router import MongoJsonEncoder

load_dotenv()
app = Flask(__name__)
CORS(app)
app.json_encoder = MongoJsonEncoder

MONGO_URI = os.environ.get("MONGO_URI")
if MONGO_URI is None:
    raise ValueError("MONGO_URI environment variable is not set")
try:
    client = MongoClient(MONGO_URI)
    db = client.farmbnb
    farm_collection = db.farm
    userfarm_collection = db.user_farm
    subscription_collection = db.subscriptions
    users = db.user
    print("Connected to MongoDB")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

##### FARMS #####


def insert_farm():
    test_farm = Farm(
        "3",
        "Farm3",
        "Farm3 description",
        "Farm3 location",
        "Farm3 area",
        12,
        "Farm3 owner",
        "Farm3 contact",
        "Farm3 farm_type",
        4.4,
    )
    farm_collection.insert_one(test_farm.__dict__)


def insert_userfarm():
    test_userfarm = UserFarm("2", "1", "2024-04-21", "2024-04-23", 40, 3)
    userfarm_collection.insert_one(test_userfarm.__dict__)


@app.route("/farm/list", methods=["GET"])
def list_farms():
    print("List of farms")
    print(request)

    farmDao = FarmDao(db)

    farmlist = farmDao.list_farms()

    print(farmlist)

    return farmlist


@app.route("/farm/<id>", methods=["GET"])
def get_farm(id):
    print("Get farm")

    farmDao = FarmDao(db)

    return farmDao.get_farm_by_id(id)


@app.route("/farm/listuserfarm", methods=["GET"])
def list_userfarms():
    user_id = request.args.get("user_id")
    print("List of user farms")
    # print(request.json)
    # insert_userfarm()

    userfarmDao = UserFarmDao(db)

    # userfarmlist = userfarmDao.list_userfarms(user_id)
    userfarmlist = userfarmDao.get_userfarm_by_userid(user_id)

    # print(userfarmlist)

    return userfarmlist


@app.route("/farm/check_availability", methods=["GET"])
def check_availability():
    print("Check availability")
    print(request.args)
    print(request.args.get("start_date"))
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    farm_id = request.args.get("farm_id")

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    print(start_date)
    print(end_date)

    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400

    if not farm_id:
        return jsonify({"error": "farm_id is required"}), 400

    userFarmDao = UserFarmDao(db)
    result = userFarmDao.get_userfarm_by_farmid(farm_id)
    if result[1] != 200:
        return jsonify({"error": result[0].json["error"]}), result[1]

    userfarms = result[0].get_json()
    for userfarm in userfarms:
        booked_start_date = datetime.strptime(userfarm["start_date"], "%Y-%m-%d").date()
        booked_end_date = datetime.strptime(userfarm["end_date"], "%Y-%m-%d").date()

        if (start_date < booked_start_date and end_date >= booked_start_date) or (
            start_date >= booked_start_date and start_date <= booked_end_date
        ):
            return jsonify({"available": False}), 200

    return jsonify({"available": True}), 200


@app.route("/farm/book", methods=["POST"])
def book_farm():
    print("Book farm")
    user_id = request.json.get("user_id")
    farm_id = request.json.get("farm_id")
    start_date = request.json.get("start_date")
    end_date = request.json.get("end_date")
    total_price = request.json.get("total_price")
    rating = 0

    if not user_id or not farm_id or not start_date or not end_date or not total_price:
        return (
            jsonify(
                {
                    "error": "user_id, farm_id, start_date, end_date, total_price are required"
                }
            ),
            400,
        )

    farmDao = FarmDao(db)
    farm = farmDao.get_farm_by_farmid(farm_id)
    print(farm)
    if farm[1] != 200:
        print("Farm not found")
        return jsonify({"error": farm[0].json["error"]}), 404

    userFarmDao = UserFarmDao(db)
    userfarm = UserFarm(user_id, farm_id, start_date, end_date, total_price, rating)
    try:
        userFarmDao.insert_userfarm(userfarm)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Farm booked successfully"}), 200


@app.route("/farm/rate", methods=["POST"])
def rate_farm():
    print("Rate farm")
    id = request.json.get("_id")
    user_id = request.json.get("user_id")
    farm_id = request.json.get("farm_id")
    rating = request.json.get("rating")

    farmDao = FarmDao(db)
    # userFarmDao = UserFarmDao(db)
    print("before")
    result = farmDao.rate_farm(farm_id, rating)
    print(result)
    if result[1] != 200:
        return jsonify({"error": result[0].json["error"]}), result[1]
    print("after")

    print("checking for rate userfarm")
    userFarmDao = UserFarmDao(db)
    result = userFarmDao.rate_userfarm(id, user_id, farm_id, rating)
    print(result)
    if result[1] != 200:
        return jsonify({"error": result[0].json["error"]}), result[1]

    return jsonify({"message": "Farm rated successfully"}), 200


##### USERS #####

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


def find_user_by_id(id):
    return users.find_one({"id": id})


@app.route("/user/login", methods=["POST"])
def login():
    credentials = request.json
    print(credentials)
    user = find_user_by_email(credentials["email"])
    password_provided = credentials["password"].encode("utf-8")

    # Converting the hashed password from string to bytes if it's not already bytes
    hashed_password_from_db = user["password"]
    if isinstance(hashed_password_from_db, str):
        hashed_password_from_db = hashed_password_from_db.encode("utf-8")
    print(user)

    if user and bcrypt.checkpw(password_provided, hashed_password_from_db):
        # Password is correct
        print("Login successful.")
        user.pop("password")
        user.pop("_id")
        return jsonify({"message": "Login successful", "user": user}), 200
    else:
        # Password is incorrect
        print("Login failed.")
        return jsonify({"message": "Invalid credentials"}), 401


@app.route("/user/register", methods=["POST"])
def register():
    user_data = request.json
    if not user_data:
        return (
            jsonify({"message": "Request data is missing or not in JSON format"}),
            400,
        )

    # Validate email
    try:
        length_for_email.handle(user_data["email"], "Email")
    except ValidationException as e:
        return jsonify({"message": str(e)}), 400

    # Check if user already exists
    if users.find_one({"email": user_data["email"]}):
        return jsonify({"message": "Email already exists"}), 400

    if users.find_one({"username": user_data["username"]}):
        return jsonify({"message": "User already exists"}), 400

    # Validate username
    try:
        length_for_username.handle(user_data["username"], "Username")
    except ValidationException as e:
        return jsonify({"message": str(e)}), 400

    # Validate password
    try:
        length_for_password.handle(user_data["password"], "Password")
    except ValidationException as e:
        return jsonify({"message": str(e)}), 400

    # Hash password
    hashed_password = bcrypt.hashpw(
        user_data["password"].encode("utf-8"), bcrypt.gensalt()
    )
    user_data["password"] = hashed_password.decode(
        "utf-8"
    )  # Store decoded hash for compatibility

    # Insert new user into the database

    users.insert_one(user_data)

    # Remove password from user details before returning it
    user_data.pop("password")
    user_data.pop("_id")
    user_data.pop("id")
    print(user_data)
    return jsonify({"message": "User registered", "user": user_data}), 201


# Profile endpoint
@app.route("/user/profile", methods=["GET"])
def profile():
    id = request.args.get("id")
    print(id)
    user = find_user_by_id(id)
    if user:
        user.pop("password")
        user.pop("_id")
        user.pop("id")
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404


# List users endpoint
@app.route("/user/list", methods=["GET"])
def list_users():
    user_list = list(users.find({}, {"password": 0}))
    print(user_list)
    for user_detail in user_list:
        user_detail.pop("_id")
        user_detail.pop("id")
    print(user_list)
    return jsonify(user_list), 200


#### PAYMENT #####

payment_dao = PaymentDao(MONGO_URI)

@app.route("/pay/book", methods=["POST"])
def process_payment_and_book():
    data = request.json
    payment = Payment(
        data.get("user_id"),
        float(data.get("amount")),
        data.get("payment_info"),
        float(data.get("total_price")),
    )
    payment_method = data.get("payment_method")
    amount = float(data.get("amount"))
    userId = data.get("user_id")

    if payment_method == "upi":
        payment_strategy = UpiPaymentStrategy()
    elif payment_method == "card":
        payment_strategy = CardPaymentStrategy()
    else:
        return jsonify({"status": "error", "message": "Invalid payment method"})

    payment_result = payment.process_payment(payment_strategy)
    return jsonify(payment_result)


@app.route("/pay/wallet", methods=["POST"])
def pay_using_wallet():
    print("paying using wallet")
    data = request.json
    user_id = data.get("user_id")
    total_price = int(data.get("total_price"))

    user = payment_dao.user_collection.find_one({"id": user_id})
    if user is None:
        return jsonify({"status": "error", "message": "User not found"})
    if user["wallet_balance"] < total_price:
        return jsonify({"status": "error", "message": "Insufficient balance"})

    payment_dao.decrease_wallet_balance(user_id, -1 * total_price)
    return jsonify({"status": "success", "message": "Payment successful using wallet"})

##### SUBSCRIPTION #####

SubscriptionManager = SubscriptionManager(subscription_collection)

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
    print(user_email)
    try:
        SubscriptionManager.addSubscription(farm_id=farm_id, user_email=user_email)
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
    app.run(port=5000)  # port for the main server
