import json
import numpy as np
import sqlite3

from flask import Flask
from flask import g
from flask_cors import CORS

from compute import compute
from keras.models import load_model
from lib.db import query_db

autoencoder = load_model('model.h5')

app = Flask(__name__)
CORS(app)


@app.before_request
def before_request():
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


@app.route('/provider')
def providers():
    res = query_db(
        'select count(ClaimID) cc, Provider, * from Outpatient group by Provider order by cc DESC LIMIT 100')

    return json.dumps(res)


@app.route('/')
def hello_world():

    # the first line of "X_test_AE"
    q = [[-2.83734569e+00,  9.83227741e-01,  2.73217562e-01, -4.78524696e-03,
          5.23113546e-02, -1.04610328e-03,  4.69188007e-02,  2.90218719e-02,
          1.25953972e-02, -3.60372131e-01,  9.00870408e-02,  7.19589387e-02,
          -7.79629676e-02, -3.79993916e-02,  1.02092528e-01, -3.35155292e-02,
          -1.48795630e-02,  1.97393418e-02, -1.22867991e-01,  4.32997898e-02,
          -1.42723225e-03, -9.13176842e-02,  1.81666606e-02, -4.26211488e-02,
          -4.27991657e-02,  4.06663542e-02,  4.96137126e-02, -4.97330536e-03,
          3.21861799e-02]]

    prediction = autoencoder.predict(np.array(q))
    return json.dumps(prediction.tolist())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
