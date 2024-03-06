import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#link provided by firewall for data base
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facerecognition-42a2d-default-rtdb.firebaseio.com/"
})

ref=db.reference('Faculty')
data={
    "001":{
        "name":"JD",
        "department":"INFORMATION TECHNOLOGY"
    }
}
#Storing the value in the data base
print("Process Stated...")
for key,value in data.items():
    ref.child(key).set(value)
print("Data added to the data base!")
