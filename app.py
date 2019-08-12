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
import base64
import datetime
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

with open("config.json") as config_file:
    config = json.load(config_file)

app.config["MAIL_SERVER"] = config["MAIL_SERVER"]
app.config["MAIL_USERNAME"] = config["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = config["MAIL_PASSWORD"]
app.config["MAIL_PORT"] = config["MAIL_PORT"]
app.config["MAIL_USE_SSL"] = config["MAIL_USE_SSL"]
app.config["MAIL_USE_TLS"] = config["MAIL_USE_TLS"] 

mail = Mail(app)
s = URLSafeTimedSerializer(config['secret_key'])

UTILS_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\utils"
IMAGE_OUTPUT_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\static\\images\\outputs"
app.config['UTILS_FOLDER'] = UTILS_FOLDER
app.config['IMAGE_OUTPUT_FOLDER'] = IMAGE_OUTPUT_FOLDER
app.secret_key = config["secret_key"]
algo = ImagifAlgorithms.Imagif(UTILS_FOLDER, IMAGE_OUTPUT_FOLDER)

def hashPassword(raw_password):
    raw_password.encode("utf-8")
    return hashlib.sha224(raw_password.encode()).hexdigest()

@app.errorhandler(404)
def error404(e):
    return render_template('error.html', message="404. The page cannot be found. I wish there was but no..."), 404

@app.errorhandler(500)
def error500(e):
    return render_template('error.html', message="500. Server error. My bad, don't give any tips..."), 500

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
        algorithmDisplayName = ""
        outputFilename = ""
        if chosenAlgorithm == 'plain':
            outputFilename = algo.use_plain(filename)
            algorithmDisplayName = "Plain"
        elif chosenAlgorithm == 'noise_switch':
            outputFilename = algo.use_noise_switch(filename)
            algorithmDisplayName = "Noise Switch"
        elif chosenAlgorithm == 'party_mode':
            outputFilename = algo.use_party_mode(filename)
            algorithmDisplayName = "Party Mode!"
        else:
            abort(500)
        os.remove(os.path.join(app.config['UTILS_FOLDER'], filename))
        time = request.form['timestamp']
        #If user logged in, store to database
        authorized = 'currentUser' in session
        if authorized:
            username = session["currentUser"]["username"]
            with psycopg2.connect(database="imagif", user="imagifcontent", password=config["imagifContent"]) as conn:
                with conn.cursor() as cur:
                    with open(os.path.join(IMAGE_OUTPUT_FOLDER, outputFilename), 'rb') as image_file:
                        cur.execute("INSERT INTO usergifs (image, username, name, algorithm ,timestamp, user_timestamp) VALUES (%s, %s, %s, %s, %s, %s)", (image_file.read(), username, outputFilename, algorithmDisplayName, datetime.datetime.now(), time))
                        print(cur.statusmessage)
                        conn.commit()
        return jsonify({"state": "success", "image" : outputFilename, "authorized" : authorized })   
    else:
        return jsonify({"state" : "error"})

@app.route("/yourgifs")
def showUserGifs():
    ##Get images from database.
    images = []
    
    with psycopg2.connect(database='imagif', user='imagifcontent', password=config["imagifContent"]) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT image, name, algorithm, user_timestamp, id FROM usergifs WHERE username=%s", (session["currentUser"]["username"],))
            print(cur.statusmessage, file=sys.stderr)
            #Reversing here so that we get a order sorted from most recent to least.
            for result in reversed(cur.fetchall()):
                images.append({ "image" : base64.b64encode(result[0]).decode("utf-8"), 
                                "name" : result[1], 
                                "algorithm" : result[2], 
                                "time" : result[3], 
                                "id" : result[4]})
      
    return render_template("usergifs.html", images=images, username=session["currentUser"]["username"])

@app.route("/login")
def loginPage():
    return render_template('auth.html')

@app.route("/logout")
def logout():
    flash('Logged out from user ' + session["currentUser"]["username"] + ".", "feedback")
    session.pop('currentUser', None)
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
                    return jsonify({"redirect" : "/", "status" : "success", "username" : result[0]})
                else:
                    return jsonify({"status" : "failure", "reason" : "password"})
            else:
                return jsonify({"status" : "failure", "reason" : "no account"})

@app.route("/confirm/<token>")
def confirmEmail(token):
    try:
        with psycopg2.connect(database="imagif", user="imagifauth", password=config["imagifAuth"]) as conn:
            with conn.cursor() as cur:
                email = s.loads(token, max_age=3600)
                cur.execute("SELECT email_confirmed FROM userinfo SET WHERE email=%s", (email,))
                email_is_confirmed = cur.fetchone()[0]
                if(email_is_confirmed):
                    return redirect(url_for('serveIndex'))
                cur.execute("UPDATE userinfo SET email_confirmed = %s WHERE email=%s", (True,email,))
                flash("Email {} has confirmed! Your gifs will be available anytime under 'Your Gifs'!'".format(email), category='feedback')
                cur.execute("SELECT username FROM userinfo WHERE email=%s", (email,))
                conn.commit()
                username = cur.fetchone()[0]
                print(username, file=sys.stderr)
                session['currentUser'] = {"username" : username}               
    except SignatureExpired:
        return render_template('error.html', message="The signature has expired.")
    except BadTimeSignature:
        return render_template('error.html', message="Bad time signature.")
    return redirect(url_for('serveIndex'))

@app.route("/handleSignup", methods=['POST'])
def handleSignup():
    response = request.get_json()
    email = response["email"]
    raw_password = response["password"]
    raw_password.encode("utf-8")
    password = hashlib.sha224(raw_password.encode())
    username = response["username"]
    user_signup_timestamp = response["joined_user_timestamp"]
    print(email, file=sys.stderr)
    try:
        with psycopg2.connect(database="imagif", user="imagifauth", password=config["imagifAuth"]) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT email, email_confirmed FROM userinfo WHERE email=%s", (email, ))
                result = cur.fetchone()
                if result:
                    #Email confirmed already.
                    if result[1]: 
                        return jsonify({'status' : 'failure', 'reason':'Already signed up', 'email' : email})
                    else:
                        sendEmailConfirmation(email)
                        return jsonify({'status' : 'failure', 'reason' : 'Email not confirmed', 'email' : email })
                cur.execute("INSERT INTO userinfo (username, email, password, joined_user_timestamp, last_sign_in, joined_user_timestamp_server, last_sign_in_server, email_confirmed) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);", 
                    (username, email, password.hexdigest(), user_signup_timestamp, user_signup_timestamp, datetime.datetime.now(), datetime.datetime.now(), False))
                conn.commit()
                sendEmailConfirmation(email)
    except psycopg2.errors.lookup(psycopg2.errorcodes.UNIQUE_VIOLATION):
        return jsonify({'status' : 'failure', 'reason':'second account with username', 'email' : email})
    return jsonify({'status' : 'success', 'message':'Email confirmation sent! Please check {}'.format(email)})

'''
Sends email confirmation.
'''
def sendEmailConfirmation(email):
    token = s.dumps(email)
    msg = Message('Confirm Email for Imagif', sender=app.config["MAIL_USERNAME"], recipients=[email])
    link = url_for('confirmEmail', token=token, _external=True)
    msg.body = "Thank you for signing up for imagif! Here is the confirmation link: \n{}".format(link)
    mail.send(msg)

@app.route("/retry-email-config", methods=['POST'])
def resendEmailConfirmation():
    email = request.args.get('email')
    sendEmailConfirmation(email)
    return jsonify({'status' : 'success', 'message':'You seem like you already signed up but you did not confirm your email. Confirmation is resent. Please check {}'.format(email), 'email' : email})

@app.route("/removegif", methods=['POST'])
def removeGif():
    client_request = request.get_json()
    try:
        with psycopg2.connect(database="imagif", user="imagifcontent", password=config["imagifContent"]) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM usergifs WHERE username=%s AND id=%s", (session["currentUser"]["username"], client_request['id']))
                flash("Deletion successful!")
                return jsonify({'status' : 'success'})
    except Exception as e:
        print(e, file=sys.stderr) 
    return jsonify({'status' : 'failure'})
    


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