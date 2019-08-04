from flask import Flask
from flask import render_template, url_for, request, redirect, session, abort, flash, jsonify, make_response, send_file
import sys
import io
import os
import utils.ImagifAlgorithms as ImagifAlgorithms
from werkzeug.utils import secure_filename
import json
import psycopg2
import psycopg2.errorcodes
import hashlib

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

with open("config.json") as config_file:
    config = json.load(config_file)

UTILS_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\utils"
IMAGE_OUTPUT_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\static\\images\\outputs"
app.config['UTILS_FOLDER'] = UTILS_FOLDER
app.config['IMAGE_OUTPUT_FOLDER'] = IMAGE_OUTPUT_FOLDER
app.secret_key = config["secret_key"]
algo = ImagifAlgorithms.Imagif(UTILS_FOLDER, IMAGE_OUTPUT_FOLDER)

def hashPassword(raw_password):
    raw_password.encode("utf-8")
    return hashlib.sha224(raw_password.encode()).hexdigest()

@app.route("/")
def serveIndex():
    if 'currentUser' in session:
        currentSession = session['currentUser']
        return render_template("index.html", username=currentSession['username'])
    else:
        return render_template("index.html")
    
@app.route("/OnImageRecieved", methods=['POST'])
def handleImage():
    if request.method == 'POST':
        try:
            inputFile = request.files['file']
        except KeyError as e:
            print(e, file=sys.stderr)
        if inputFile == None:
            return render_template("index.html", convertedGif=False)
        print("Hello " + inputFile.filename, file=sys.stderr)
        filename = secure_filename(inputFile.filename)
        inputFile.save(os.path.join(app.config['UTILS_FOLDER'], filename))
        chosenAlgorithm = request.form['algorithm']
        outputFilename = ""
        if chosenAlgorithm == 'plain':
            outputFilename = algo.use_plain(filename)
        elif chosenAlgorithm == 'noise_switch':
            outputFilename = algo.use_noise_switch(filename)
        elif chosenAlgorithm == 'party_mode':
            outputFilename = algo.use_party_mode(filename)
        else:
            abort(500)
        #TODO: Flash message saying that the gif is saved under my gifs.
        os.remove(os.path.join(app.config['UTILS_FOLDER'], filename))
        #If user logged in, store to database
        if 'currentUser' in session:
            username = session["currentUser"]["username"]
            with psycopg2.connect(database="imagif", user="imagifcontent", password=config["imagifContent"]) as conn:
                with conn.cursor() as cur:
                    with open(os.path.join(IMAGE_OUTPUT_FOLDER, outputFilename), 'rb') as image_file:
                        cur.execute("INSERT INTO usergifs (image, username) VALUES (%s, %s)", (image_file.read(), username))
                        print(cur.statusmessage)
                        conn.commit()
                        flash("Image saved in 'Your Gifs'", "feedback")

        return jsonify({"state": "success", "image" : outputFilename })   
    else:
        return jsonify({"state" : "error"})

@app.route("/login")
def loginPage():
    return render_template('auth.html')

@app.route("/logout")
def logout():
    session.pop('currentUser', None)
    flash('Logged out from user ' + session["currentUser"]["username"] + ".", "feedback")
    return redirect(url_for('serveIndex'))

#TODO: Handle login, add to database after sign up, bring the list of gifs from the database.
@app.route("/handleLogin", methods=['POST'])
def handleLogin():
    login_response = request.get_json()
    email = login_response["email"]
    password = login_response["password"]
    with psycopg2.connect(database="imagif", user="imagifauth", password=config["imagifAuth"]) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM userinfo WHERE email = %s;", (email,))
            result = cur.fetchone()
            if result:
                if result[2] == hashPassword(password):
                    session['currentUser'] = {"username" : result[0], "id" : result[3]}
                    return jsonify({"redirect" : "/", "status" : "success"})
                else:
                    return jsonify({"status" : "failure", "reason" : "password"})
            else:
                return jsonify({"status" : "failure", "reason" : "no account"})

@app.route("/handleSignup", methods=['POST'])
def handleSignup():
    response = request.get_json()
    email = response["email"]
    raw_password = response["password"]
    raw_password.encode("utf-8")
    password = hashlib.sha224(raw_password.encode())
    username = response["username"]
    print(email, file=sys.stderr)
    try:
        with psycopg2.connect(database="imagif", user="imagifauth", password=config["imagifAuth"]) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO userinfo VALUES (%s,%s,%s);", (username, email, password.hexdigest()))
                cur.execute("SELECT currval(pg_get_serial_sequence('userinfo','id'));")
                user_id = cur.fetchone()
                conn.commit()
                session['currentUser'] = {"username" : username ,  "id" : user_id[0]}
                flash('Sign up successful for ' + username + '!' +" Your gifs will be available anytime under 'Your Gifs'!", "feedback")
    except psycopg2.errors.lookup(psycopg2.errorcodes.UNIQUE_VIOLATION):
        return jsonify({'status' : 'failure', 'reason':'second account with email', 'email' : email})
    finally:
        cur.close()
        conn.close()
    return jsonify({'status' : 'success', 'redirect' : '/'})

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