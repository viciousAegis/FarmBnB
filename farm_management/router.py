from flask import Flask

app = Flask(__name__)

@app.route("/farm/list", methods=["GET"])
def list_farms():
    return "List of farms"

if __name__ == "__main__":
    app.run()