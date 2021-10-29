import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Fetch service account key JSON file contents
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


data = {"name" : "Shawn", "age" : "23"}

db.collection('people').add(data)