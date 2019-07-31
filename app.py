from flask import Flask
from flask import render_template, url_for, request, redirect, session, abort, flash, jsonify, make_response, send_file
import sys
import io
import os
import utils.ImagifAlgorithms as ImagifAlgorithms
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

projectID = "https://imagif-199a8.firebaseio.com/"
#firebase = firebase.FirebaseApplication(projectID, None)

UTILS_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\utils"
IMAGE_OUTPUT_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\static\\images\\outputs"
app.config['UTILS_FOLDER'] = UTILS_FOLDER
app.config['IMAGE_OUTPUT_FOLDER'] = IMAGE_OUTPUT_FOLDER
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsw5'
algo = ImagifAlgorithms.Imagif(UTILS_FOLDER, IMAGE_OUTPUT_FOLDER)

@app.route("/")
def serveIndex():
    if 'currentUser' in session:
        return render_template("index.html", username=session['currentUser'])
    else:
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
        outputFilename = ""
        if chosenAlgorithm == 'plain':
            outputFilename = algo.use_plain(filename)
            print(outputFilename, file=sys.stderr)
        elif chosenAlgorithm == 'noise_switch':
            outputFilename = algo.use_noise_switch(filename)
            print(outputFilename, file=sys.stderr)
        elif chosenAlgorithm == 'party_mode':
            outputFilename = algo.use_party_mode(filename)
            print(outputFilename, file=sys.stderr)
        else:
            abort(500)
        os.remove(os.path.join(app.config['UTILS_FOLDER'], filename))
        return jsonify({"state": "success", "image" : outputFilename })   
    else:
        return jsonify({"state" : "error"})
@app.route("/login")
def loginPage():
    return render_template('auth.html')

#TODO: Handle login, add to database after sign up, bring the list of gifs from the database.
@app.route("/handleLogin", methods=['POST'])
def handleLogin():
    print(request.is_json, file=sys.stderr)
    login_response = request.get_json()
    email = login_response["email"]
    password = login_response["password"]
    print("Logged in as: " + email, file=sys.stderr)
    session['currentUser'] = email
    return jsonify({"redirect" : "/"})
    #Add email to database if doesn't exist. Actually do that in signup.

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
