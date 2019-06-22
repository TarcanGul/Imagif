from flask import Flask
from flask import render_template, url_for, request, redirect
app = Flask(__name__)

@app.route("/")
def serveIndex():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
