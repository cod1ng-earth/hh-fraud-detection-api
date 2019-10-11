import json

import sqlite3
import os.path

from flask import Flask
from flask import g
from flask import request
from flask import Response
from flask_cors import CORS
from flask import flash, render_template, redirect, url_for

from lib.db import query_db
from lib.compute import callModel
from urllib.request import urlretrieve
import random

import csv
from werkzeug.utils import secure_filename
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'Uploads'
ALLOWED_EXTENSIONS = set(['csv', 'Json'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] ='Blub'

@app.before_request
def before_request():
    if not os.path.isfile("claims.db"):
        urlretrieve("http://stadolf.de/claims.db", "claims.db")

    g.db = sqlite3.connect(
        "claims.db"
    )


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/provider/<providerId>/claims')
def provider(providerId):

    res = query_db(
        'select * from Outpatient i left join Beneficiary B on i.BeneID = B.BeneID where Provider= ?', (providerId,))
    return json.dumps(res)


@app.route('/provider/<providerId>/fraud')
def provider_fraud(providerId):

    res = query_db(
        'select * from Fraud where Provider= ?', (providerId,))
    return json.dumps(res)


# yields providers with around 300 claims
@app.route('/provider')
def providers():
    sql = """
    select count(ClaimID) cc, o.Provider, F.PotentialFraud
    from Outpatient o
    left join Fraud F on o.Provider = F.Provider
    group by o.Provider
    order by cc
    DESC LIMIT 100 offset 1500;
    """
    res = query_db(sql)

    return json.dumps(res)


@app.route('/check-fraud', methods=['POST'])
def checkFraud2():
    claims = request.get_json()
    result = callModel(claims)

    # now, just mock it
    result = {'fraud': random.random()}

    return Response(json.dumps(result), mimetype='application/json')

#def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''       

@app.route('/parseCSVToJSON')
def checkFraud():

    f = open( '/Uploads/CSVTest.csv', 'rU' ) 
    reader = csv.DictReader( f, fieldnames = ( "fieldname0","fieldname1","fieldname2","fieldname3" ))  
    parsedCsvToJson = json.dumps( [ row for row in reader ] )   
    f = open( 'CSVTest.json', 'w')  
    f.write(parsedCsvToJson)   


    claims = request.get_json()
    result = callModel(claims)

    # now, just mock it
    result = {'fraud': random.random()}
    return Response(json.dumps(result), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
