import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import json

# located in scripts folder
from scripts.timestamp import get_timestamp
from scripts.csv_to_json import csv_to_json

# possible to add extra formats for later
UPLOAD_FOLDER = './temp/'
OUTPUT_FORMATS = ['csv']

# check if the format of file is in allowed formats
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in OUTPUT_FORMATS


# start app
app = Flask(__name__)

# set upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# stop jsonify from sorting the output
app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request requires a file
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            # for security
            filename = secure_filename(file.filename)

            # timestamp for storing unique output
            timestamp = get_timestamp()

            # upload csv
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], timestamp))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], timestamp, filename))

            delimiter = request.form.get('delimiters')

            # converts csv file to json and upload to timestamped folder
            csv_to_json(app.config['UPLOAD_FOLDER'], timestamp, filename, delimiter)

            # clean-up (delete csv file since conversion is done)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], timestamp, filename))

            return redirect(url_for("view_json", timestamp=timestamp))

    return render_template("form.html", formats = ", ".join(OUTPUT_FORMATS))

@app.route('/temp/<timestamp>/output.json')
def view_json(timestamp):
    
    filename = "output.json"

    with open(os.path.join(app.config['UPLOAD_FOLDER'], timestamp, filename)) as file:
        data = json.load(file)

    return data

if __name__ == '__main__':
    app.run()