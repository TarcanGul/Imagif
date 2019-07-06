from flask import Flask
from flask import render_template, url_for, request, redirect, session
import sys
import io
import os
import utils.ImagifAlgorithms as ImagifAlgorithms
from werkzeug.utils import secure_filename

app = Flask(__name__)
exportedGif = False


UTILS_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\utils"
app.config['UTILS_FOLDER'] = UTILS_FOLDER
app.config['IMAGE_OUTPUT_FOLDER'] = os.path.dirname(os.path.realpath(__file__)) + "\\static\\images"
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsw5'
algo = ImagifAlgorithms.Imagif(UTILS_FOLDER, app.config['IMAGE_OUTPUT_FOLDER'])

@app.route("/")
def serveIndex():
    print("convertedGif" in session, file=sys.stderr)
    if "convertedGif" in session:
        print(session.get("convertedGif"), file=sys.stderr)
        return render_template("index.html", convertedGif=session.get("convertedGif"))
    else:
        return render_template("index.html", convertedGif=False)
   
    

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
    session["convertedGif"]= True
    return redirect(url_for("serveIndex"))   

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
