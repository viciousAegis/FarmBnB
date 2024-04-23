from flask import Flask, jsonify, request
import subprocess
import requests

app = Flask(__name__)

@app.route('/farm/<path:subpath>', methods=['GET', 'POST'])
def run_farm(subpath):
    farm_port = 5001
    
    farm_process = subprocess.Popen(['python3', 'farm_management/router.py'])
    
    # Check if the server is running by making a request to the health check endpoint
    farm_health_url = f'http://127.0.0.1:{farm_port}/health'
    while True:
        try:
            response = requests.get(farm_health_url)
            print(response.text)
            if response.text == 'OK':
                break  # Server is up and running
        except requests.ConnectionError:
            pass  # Server is not yet available, try 
    request = {
        "json": {
            "key": "value"
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }   

    farm_url = f'http://localhost:{farm_port}/farm/{subpath}'
    farm_response = requests.post(farm_url, json=request["json"], headers=request["headers"])
    
    # terminate the farm server
    farm_process.terminate()
    
    return farm_response.json()

if __name__ == '__main__':
    app.run(port=5000) # port for the main server
    