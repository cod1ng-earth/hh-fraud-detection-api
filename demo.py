import json

import sqlite3
import os.path

#from lib.compute import callModel
from urllib.request import urlretrieve
import random

from transform import transform


def query_db(query, args=(), one=False):
    db = sqlite3.connect("claims.db")
    cur = db.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]

    # cur.connection.close()
    return (r[0] if r else None) if one else r


if __name__ == '__main__':
    if not os.path.isfile("claims.db"):
        urlretrieve("http://stadolf.de/claims.db", "claims.db")

    providerId = 'PRV56156'
    res = query_db(
        'select * from Outpatient i left join Beneficiary B on i.BeneID = B.BeneID where Provider= ? limit 3', (providerId,))

    print(res[0])
    #r = json.dumps(res)

    # print(r)
