import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from payment import Payment
from payment_strategy import UpiPaymentStrategy, CardPaymentStrategy
from paymentDao import PaymentDao

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get("MONGO_URI")
if MONGO_URI is None:
    raise ValueError("MONGO_URI environment variable is not set")

payment_dao = PaymentDao(MONGO_URI)

'''
this is the health check endpoint for the farm server.
this is used to check if the farm server is running.
'''
@app.route('/health')
def health_check():
    return 'OK'

@app.route("/pay/book", methods=["POST"])
def process_payment_and_book():
    data = request.json
    payment = Payment(data.get("user_id"), data.get("total_price"), data.get("payment_info"))
    payment_method = data.get("payment_method")

    if payment_method == "upi":
        payment_strategy = UpiPaymentStrategy()
    elif payment_method == "card":
        payment_strategy = CardPaymentStrategy()
    else:
        return jsonify({"status": "error", "message": "Invalid payment method"})

    payment_result = payment.process_payment(payment_strategy)
    if payment_result["status"] == "success":
        payment_dao.update_wallet_balance(data["user_id"], -data["total_price"])
        return jsonify(payment_result)
    else:
        return jsonify({"status": "error", "message": f"Payment using {payment_method} failed"})

@app.route('/pay/wallet', methods=['POST'])
def pay_using_wallet():
    data = request.json
    user_id = data.get("user_id")
    total_price = int(data.get("total_price"))

    user = payment_dao.user_collection.find_one({"user_id": user_id})
    if user is None:
        return jsonify({"status": "error", "message": "User not found"})
    if user["wallet_balance"] < total_price:
        return jsonify({"status": "error", "message": "Insufficient balance"})
    
    payment_dao.update_wallet_balance(user_id, -total_price)
    return jsonify({"status": "success", "message": "Payment successful using wallet"})

@app.route('/health')
def health_check():
    return "OK"

if __name__ == "__main__":
    app.run(debug=False, port=5002)
