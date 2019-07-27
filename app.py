from flask import Flask
from flask import render_template, url_for, request, redirect, session, abort, flash, jsonify, make_response, send_file
import sys
import io
import os
import utils.ImagifAlgorithms as ImagifAlgorithms
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

UTILS_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\utils"
app.config['UTILS_FOLDER'] = UTILS_FOLDER
app.config['IMAGE_OUTPUT_FOLDER'] = os.path.dirname(os.path.realpath(__file__)) + "\\static\\images"
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsw5'
algo = ImagifAlgorithms.Imagif(UTILS_FOLDER, UTILS_FOLDER + "\\outputs")

@app.route("/")
def serveIndex():
    return render_template("index.html")
    
@app.route("/OnImageRecieved", methods=['POST'])
def handleImage():
    if request.method == 'POST':
        print(request.form, file=sys.stderr)
        try:
            inputFile = request.files['file']
        except KeyError as e:
            print(e, file=sys.stderr)
        if inputFile == None:
            return render_template("index.html", convertedGif=False)
        print("Hello " + inputFile.filename, file=sys.stderr)
        filename = secure_filename(inputFile.filename)
        inputFile.save(os.path.join(app.config['UTILS_FOLDER'], filename))
        print(type(inputFile), file=sys.stderr)
        print(filename, file=sys.stderr)
        print(algo.get_read_dir(), file=sys.stderr)
        chosenAlgorithm = request.form['algorithm']
        if chosenAlgorithm == 'plain':
            print(algo.use_plain(filename), file=sys.stderr)
        elif chosenAlgorithm == 'noise_switch':
            print(algo.use_noise_switch(filename), file=sys.stderr)
        else:
            abort(500)
        os.remove(os.path.join(app.config['UTILS_FOLDER'], filename))
        return jsonify({"state": "success", "image" : "blue" })   
    else:
        return jsonify({"state" : "error"})

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
