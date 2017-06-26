from flask import *

app = Flask(__name__)

@app.route("/index")
def hello_world():
    return "Not Hello world"

if __name__ == "__main__":
    app.run()
