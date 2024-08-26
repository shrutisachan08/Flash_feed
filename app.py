from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return "Hello"

if __name__ == '_main_':
    app.run(debug = True, port = 5001)