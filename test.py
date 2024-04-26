

from concurrent.futures import ThreadPoolExecutor
from flask import jsonify
import requests
from time import time
from random import randint
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:5000"

def get_random_date():
    year = randint(2022, 2025)
    month = randint(1, 12)
    day = randint(1, 28)
    
    return f"{year}-{month:02d}-{day:02d}"

def get_next_date(date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    next_date = date_obj + timedelta(days=1)
    return next_date.strftime("%Y-%m-%d")

def book_farm():
    user = "ug85hjds9"
    farm_id = "2"
    # get random start date

    start_date = get_random_date()  # Example date, replace with actual date
    # book for 2 days
    end_date = get_next_date(start_date)  # Example date, replace with actual date
    
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

def list_farms():
    start_time = time()
    response = requests.get(f"{BASE_URL}/farm/list")
    elapsed_time = time() - start_time
    if response.ok:
        data = response.json()
        code = response.status_code
        return data, code, elapsed_time
    else:
        return None, response.status_code, elapsed_time

def concurrent_test():
    st = time()
    NUM_REQUESTS = 100  # Number of concurrent requests to send

    # Function to make requests
    def make_request():
        res, code = book_farm()
        print(res, code)
        return res, code

    # Send concurrent requests
    with ThreadPoolExecutor(max_workers=NUM_REQUESTS) as executor:
        futures = [executor.submit(make_request) for _ in range(NUM_REQUESTS)]

    # Wait for all futures to complete
    for future in futures:
        future.result()

    total_elapsed_time = time() - st
    
    # Calculate throughput
    total_requests = NUM_REQUESTS
    throughput = total_requests / total_elapsed_time
    print("Throughput:", throughput, "requests/second")
    print("Total Time taken:", total_elapsed_time)
    print("Average Response Time:", total_elapsed_time / total_requests)

def normal_test():
    st = time()
    res, code, elapsed_time = list_farms()
    print(res, code)
    total_elapsed_time = time() - st
    print("Total Time taken:", total_elapsed_time)
    
if __name__ == "__main__":
    # normal_test()
    concurrent_test()