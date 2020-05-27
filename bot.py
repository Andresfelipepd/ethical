import json
import urllib2
url = "https://api.tidex.com/api/3/ticker/eth_btc"


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("keyDB.json")
firebase_admin.initialize_app(cred)
db = firestore.Client()
for i in range(0,10):
    response = urllib2.urlopen(url)
    data = response.read()
    values = json.loads(data)
    print(values)
    db.collection('datos_btc').document(str(i)).set(values)