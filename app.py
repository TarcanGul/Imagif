from flask import Flask
from flask import render_template, url_for, request, redirect
import sys
import io
import os
import utils.ImagifAlgorithms as algo
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def serveIndex():
    return render_template("index.html")

@app.route("/OnImageRecieved", methods=['POST'])
def handleImage():
    inputFile = request.files['file']
    print("Hello " + inputFile.filename, file=sys.stderr)
    filename = secure_filename(inputFile.filename)
    inputFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    algo.use_noise_switch(inputFile.filename)
    return "Success."    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
