from flask import Flask
from flask import render_template, url_for, request, redirect
import sys
import io
import os
import utils.ImagifAlgorithms as ImagifAlgorithms
from werkzeug.utils import secure_filename

app = Flask(__name__)

UTILS_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\utils"
app.config['UTILS_FOLDER'] = UTILS_FOLDER

algo = ImagifAlgorithms.Imagif(UTILS_FOLDER)

@app.route("/")
def serveIndex():
    return render_template("index.html")

@app.route("/OnImageRecieved", methods=['POST'])
def handleImage():
    inputFile = request.files['file']
    print("Hello " + inputFile.filename, file=sys.stderr)
    filename = secure_filename(inputFile.filename)
    inputFile.save(os.path.join(app.config['UTILS_FOLDER'], filename))
    print(type(inputFile), file=sys.stderr)
    print(filename, file=sys.stderr)
    print(algo.get_target_dir(), file=sys.stderr)
    algo.use_noise_switch(filename, "output.gif")
    os.remove(os.path.join(app.config['UTILS_FOLDER'], filename))
    return "Success."    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
