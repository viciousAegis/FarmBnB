

from flask import jsonify
import requests
from time import time

BASE_URL = "http://127.0.0.1:5000"

def book_farm():
    user = "ug85hjds9"
    farm_id = "2"
    start_date = "2025-04-28"  # Example date, replace with actual date
    end_date = "2025-04-29"    # Example date, replace with actual date
    total_price = 1  # Example price, replace with actual price

    if not start_date or not end_date:
        return {"error": "Please select start and end dates to book"}, 400

    wallet_balance = fetch_user_profile(user)
    if wallet_balance is None:
        return {"error": "Error fetching user profile"}, 500

    if wallet_balance < total_price:
        return {"error": "Insufficient balance"}, 400

    payment_status = make_wallet_payment(user, total_price)
    if payment_status != "success":
        return {"error": "Error paying using wallet"}, 500

    booking_status = book_farm_request(user, farm_id, start_date, end_date, total_price)
    if booking_status != "success":
        return {"error": "Error booking farm"}, 500

    notification_status = send_notification(farm_id, start_date, end_date)
    if notification_status != "success":
        return {"error": "Error sending notification"}, 500

    return {"message": "Farm booked successfully"}, 200


def fetch_user_profile(user_id):
    response = requests.get(f"{BASE_URL}/user/profile?id={user_id}")
    if response.ok:
        data = response.json()
        return data.get("wallet_balance")
    else:
        return None


def make_wallet_payment(user_id, total_price):
    payload = {"user_id": user_id, "total_price": total_price}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{BASE_URL}/pay/wallet", json=payload, headers=headers)
    if response.ok:
        data = response.json()
        return data.get("status")
    else:
        return None


def book_farm_request(user_id, farm_id, start_date, end_date, total_price):
    payload = {
        "user_id": user_id,
        "farm_id": farm_id,
        "start_date": start_date,
        "end_date": end_date,
        "total_price": total_price
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{BASE_URL}/farm/book", json=payload, headers=headers)
    if response.ok:
        return "success"
    else:
        return None


def send_notification(farm_id, start_date, end_date):
    payload = {
        "farm_id": farm_id,
        "message": f"Farm {farm_id} has been booked from {start_date} to {end_date}"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{BASE_URL}/subscription/notify", json=payload, headers=headers)
    if response.ok:
        return "success"
    else:
        return None
    
if __name__ == "__main__":
    st = time()
    res, code = book_farm()
    print(res, code)
    print("Time taken:", time()-st)