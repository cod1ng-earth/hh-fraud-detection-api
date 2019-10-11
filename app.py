import json

import sqlite3
import os.path

from flask import Flask
from flask import g
from flask import request
from flask import Response
from flask_cors import CORS

from lib.db import query_db
from lib.compute import callModel
from urllib.request import urlretrieve
import random

app = Flask(__name__)
CORS(app)


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
def checkFraud():
    claims = request.get_json()
    result = callModel(claims)

    # now, just mock it
    result = {'fraud': random.random()}

    return Response(json.dumps(result), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
