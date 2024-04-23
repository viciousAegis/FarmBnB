from flask import Flask, request

app = Flask(__name__)

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