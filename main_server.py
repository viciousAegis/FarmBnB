from flask import Flask, jsonify, request
import subprocess
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def create_query_string(url, args):
    # args is an immutable dictionary
    query_string = ""
    for key, value in args.items():
        query_string += f"{key}={value}&"
    query_string = query_string[:-1]  # remove the last '&'
    return f"{url}?{query_string}"

@app.route("/farm/<path:subpath>", methods=["GET", "POST"])
def run_farm(subpath):
    print("starting farm server")
    farm_port = 5001
    
    # check if its already running
    try:
        farm_health_url = f"http://127.0.0.1:{farm_port}/health"
        response = requests.get(farm_health_url)
        if response.text == "OK":
            pass
    except requests.ConnectionError:
        farm_process = subprocess.Popen(["python3", "farm_management/router.py"])

    # Check if the server is running by making a request to the health check endpoint
    farm_health_url = f"http://127.0.0.1:{farm_port}/health"
    while True:
        try:
            response = requests.get(farm_health_url)
            print(response.text)
            if response.text == "OK":
                break  # Server is up and running
        except requests.ConnectionError:
            pass  # Server is not yet available, try
    print("farm server is running")
    farm_url = f"http://localhost:{farm_port}/farm/{subpath}"

    # check method type
    if request.method == "GET":
        if request.args:
            farm_url = create_query_string(farm_url, request.args)
        print(farm_url)
        farm_response = requests.get(farm_url, headers=request.headers)
    elif request.method == "POST":
        farm_response = requests.post(
            farm_url, json=request.json, headers=request.headers
        )

    # terminate the farm server
    # farm_process.terminate()
    # print("closing farm server")

    return farm_response.json()


@app.route("/user/<path:subpath>", methods=["GET", "POST"])
def run_user(subpath):
    print("starting user server")
    user_port = 5004

    user_process = subprocess.Popen(["python3", "user/router.py"])

    # Check if the server is running by making a request to the health check endpoint
    user_health_url = f"http://127.0.0.1:{user_port}/health"
    while True:
        try:
            response = requests.get(user_health_url)
            print(response.text)
            if response.text == "OK":
                break  # Server is up and running
        except requests.ConnectionError:
            pass

    print("user server is running")
    user_url = f"http://localhost:{user_port}/user/{subpath}"
    if request.method == "GET":
        if request.args:
            user_url = create_query_string(user_url, request.args)
        user_response = requests.get(user_url, json=request.json, headers=request.headers)
    elif request.method == "POST":
        user_response = requests.post(
            user_url, json=request.json, headers=request.headers
        )

    # terminate the user server
    print("closing user server")
    user_process.terminate()

    return user_response.json()


@app.route("/pay/<path:subpath>", methods=["GET", "POST"])
def run_payment(subpath):
    print("starting payment server")
    payment_port = 5002

    payment_process = subprocess.Popen(["python3", "payment/router.py"])

    # Check if the server is running by making a request to the health check endpoint
    payment_health_url = f"http://127.0.0.1:{payment_port}/health"
    while True:
        try:
            response = requests.get(payment_health_url)
            print(response.text)
            if response.text == "OK":
                break  # Server is up and running
        except requests.ConnectionError:
            pass

    print("payment server is running")
    payment_url = f"http://localhost:{payment_port}/pay/{subpath}"
    if request.method == "GET":
        if request.args:
            payment_url = create_query_string(payment_url, request.args)
        payment_response = requests.get(payment_url, json=request.json, headers=request.headers)
    elif request.method == "POST":
        payment_response = requests.post(
            payment_url, json=request.json, headers=request.headers
        )

    # terminate the payment server
    print("closing payment server")
    payment_process.terminate()

    return payment_response.json()


if __name__ == "__main__":
    app.run(port=5000)  # port for the main server
