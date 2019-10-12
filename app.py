import json

import sqlite3
import os.path

from flask import Flask
from flask import g
from flask import request
from flask import Response
from flask_cors import CORS

from lib.db import query_db, all_claims, all_claims_x
from lib.compute import callModel, featurize
from urllib.request import urlretrieve


import random
import pandas as pd
import numpy as np

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
    claims = all_claims(providerId)
    return json.dumps(claims)


@app.route('/provider/<providerId>/check-fraud')
def provider_check_fraud(providerId):
    claims = pd.DataFrame(all_claims_x(providerId))

    claims = claims.replace({'ChronicCond_Alzheimer': 2, 'ChronicCond_Heartfailure': 2, 'ChronicCond_KidneyDisease': 2,
                             'ChronicCond_Cancer': 2, 'ChronicCond_ObstrPulmonary': 2, 'ChronicCond_Depression': 2,
                             'ChronicCond_Diabetes': 2, 'ChronicCond_IschemicHeart': 2, 'ChronicCond_Osteoporasis': 2,
                             'ChronicCond_rheumatoidarthritis': 2, 'ChronicCond_stroke': 2}, 0)
    claims = claims.replace("NA", "NaN")
    claims = claims.replace({'RenalDiseaseIndicator': 'Y'}, 1)

    claims['DOB'] = pd.to_datetime(claims['DOB'], format='%Y-%m-%d')
    claims['DOD'] = pd.to_datetime(
        claims['DOD'], format='%Y-%m-%d', errors='ignore')
    claims['Age'] = round(((claims['DOD'] - claims['DOB']).dt.days)/365)
    claims.Age.fillna(round(((pd.to_datetime('2009-12-01', format='%Y-%m-%d') - claims['DOB']).dt.days)/365),
                      inplace=True)

    claims.loc[claims.DOD.isna(), 'WhetherDead'] = 0
    claims.loc[claims.DOD.notna(), 'WhetherDead'] = 1

    claims['AdmissionDt'] = pd.to_datetime(
        claims['AdmissionDt'], format='%Y-%m-%d')
    claims['DischargeDt'] = pd.to_datetime(
        claims['DischargeDt'], format='%Y-%m-%d')
    claims['AdmitForDays'] = (
        (claims['DischargeDt'] - claims['AdmissionDt']).dt.days)+1
    claims = featurize(claims)

    cols1 = claims.select_dtypes([np.number]).columns
    cols2 = claims.select_dtypes(exclude=[np.number]).columns
    claims[cols1] = claims[cols1].fillna(value=0)
    cols = claims.columns

    remove_these_columns = ['BeneID', 'ClaimID', 'ClaimStartDt', 'ClaimEndDt', 'AttendingPhysician',
                            'OperatingPhysician', 'OtherPhysician', 'ClmDiagnosisCode_1',
                            'ClmDiagnosisCode_2', 'ClmDiagnosisCode_3', 'ClmDiagnosisCode_4',
                            'ClmDiagnosisCode_5', 'ClmDiagnosisCode_6', 'ClmDiagnosisCode_7',
                            'ClmDiagnosisCode_8', 'ClmDiagnosisCode_9', 'ClmDiagnosisCode_10',
                            'ClmProcedureCode_1', 'ClmProcedureCode_2', 'ClmProcedureCode_3',
                            'ClmProcedureCode_4', 'ClmProcedureCode_5', 'ClmProcedureCode_6',
                            'ClmAdmitDiagnosisCode', 'AdmissionDt',
                            'DischargeDt', 'DiagnosisGroupCode', 'DOB', 'DOD',
                            'State', 'County']
    claims = claims.drop(axis=1, columns=remove_these_columns)
    claims.Gender = claims.Gender.astype('category')
    claims.Race = claims.Race.astype('category')
    claims = pd.get_dummies(
        claims, columns=['Gender', 'Race'], drop_first=True)

    claims = claims.loc[:, ['Provider', "Age", "Gender_2", "InscClaimAmtReimbursed", "ClmCount_Provider_ClmProcedureCode_1",	"ClmCount_Provider_ClmProcedureCode_2",	"ClmCount_Provider_ClmProcedureCode_3",	"ClmCount_Provider_ClmProcedureCode_4",	"ClmCount_Provider_ClmProcedureCode_5",	"ClmCount_Provider_ClmDiagnosisCode_1",
                            "ClmCount_Provider_ClmDiagnosisCode_2",	"ClmCount_Provider_ClmDiagnosisCode_3",	"ClmCount_Provider_ClmDiagnosisCode_4",	"ClmCount_Provider_ClmDiagnosisCode_5",	"ClmCount_Provider_ClmDiagnosisCode_6", "ClmCount_Provider_ClmDiagnosisCode_7", "ClmCount_Provider_ClmDiagnosisCode_8", "ClmCount_Provider_ClmDiagnosisCode_9", "DeductibleAmtPaid", "AdmitForDays"]]
    claims = claims.groupby(['Provider'], as_index=False).agg('mean')
#    return claims.to_json(orient="records")

    X = claims.drop(axis=1, columns=['Provider'])

    result = callModel(X)

    return json.dumps(result.tolist())
    # return X_std.to_json(orient="records")


@app.route('/provider/<providerId>/fraud')
def provider_fraud(providerId):

    res = query_db(
        'select * from Fraud where Provider= ?', (providerId,))
    return json.dumps(res)


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
