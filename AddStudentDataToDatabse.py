import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#link provided by firewall for data base
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facerecognition-42a2d-default-rtdb.firebaseio.com/"
})

ref=db.reference('Students')        #creating the directory reference in the DB

data={                              #Storing the value in Json formate in key Value type
    "73771111":{
        "name":"TAMILMANI S",
        "major":"INFORMATION TECHNOLOGY",
        "section":"A",
        "year":"I",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":3
    },
    "73771112":{
        "name":"PRASATH S",
        "major":"INFORMATION TECHNOLOGY",
        "section":"A",
        "year":"I",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":4
    },
    "73771121":{
        "name":"SANJAYKUMAR V",
        "major":"INFORMATION TECHNOLOGY",
        "section":"A",
        "year":"I",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":2
    },
    "73771122":{
        "name":"VASANTHAN R",
        "major":"INFORMATION TECHNOLOGY",
        "section":"A",
        "year":"I",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":6
    },
    "73771211":{
        "name":"SURYA M",
        "major":"INFORMATION TECHNOLOGY",
        "section":"A",
        "year":"II",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":2
    },
    "73771212":{
        "name":"SUBASH S",
        "major":"INFORMATION TECHNOLOGY",
        "section":"A",
        "year":"II",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":8
    },
    "73771221":{
        "name":"PARVESH AHAMED J",
        "major":"INFORMATION TECHNOLOGY",
        "section":"B",
        "year":"II",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":9
    },
    "73771222":{
        "name":"SUVINKUMAR P",
        "major":"INFORMATION TECHNOLOGY",
        "section":"B",
        "year":"II",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":4
    },
    "73771311":{
        "name":"PRAVEEN S",
        "major":"INFORMATION TECHNOLOGY",
        "section":"A",
        "year":"III",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":10
    },
    "73771312":{
        "name":"VEERAGOKULRAJ S",
        "major":"INFORMATION TECHNOLOGY",
        "section":"A",
        "year":"III",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":11
    },
    "73771321":{
        "name":"SANJAY S",
        "major":"INFORMATION TECHNOLOGY",
        "section":"B",
        "year":"III",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":3
    },
    "73771322":{
        "name":"RISHWANTH R",
        "major":"INFORMATION TECHNOLOGY",
        "section":"B",
        "year":"III",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":4
    },
    "73771411":{
        "name":"ASHALESHWARAN VM",
        "major":"INFORMATION TECHNOLOGY",
        "section":"A",
        "year":"VI",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":2
    },
    "73771412":{
        "name":"HARISH V",
        "major":"INFORMATION TECHNOLOGY",
        "section":"A",
        "year":"VI",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":6
    },
    "73771421":{
        "name":"VIGNESHWARAN K",
        "major":"INFORMATION TECHNOLOGY",
        "section":"B",
        "year":"VI",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":2
    },
    "73771422":{
        "name":"SUJITH S",
        "major":"INFORMATION TECHNOLOGY",
        "section":"B",
        "year":"VI",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":8
    },
    "73772111":{
        "name":"BALABARATHI V",
        "major":"COMPUTER SCIENCE",
        "section":"A",
        "year":"I",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":9
    },
    "73772121":{
        "name":"CIBI M",
        "major":"COMPUTER SCIENCE",
        "section":"B",
        "year":"I",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":11
    },
    "73772211":{
        "name":"AAKASK K",
        "major":"COMPUTER SCIENCE",
        "section":"A",
        "year":"II",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":11
    },
    "73772221":{
        "name":"DINESH K",
        "major":"COMPUTER SCIENCE",
        "section":"B",
        "year":"II",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":4
    },
    "73772311":{
        "name":"VASIGARAN P",
        "major":"COMPUTER SCIENCE",
        "section":"A",
        "year":"III",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":11
    },
    "73772321":{
        "name":"RANJITH K",
        "major":"COMPUTER SCIENCE",
        "section":"B",
        "year":"III",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":4
    },
    "73772411":{
        "name":"ARUNACHELLAM P",
        "major":"COMPUTER SCIENCE",
        "section":"A",
        "year":"IV",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":11
    },
    "73772421":{
        "name":"SANTOSHKUMAR JV",
        "major":"COMPUTER SCIENCE",
        "section":"B",
        "year":"IV",
        "last_seeked":"2023-10-14 00:54:34",
        "numberOf_time_seeked":11
    }
}
#Storing the value in the data base
print("Process Stated...")
for key,value in data.items():
    ref.child(key).set(value)
print("Data added to the data base!")
