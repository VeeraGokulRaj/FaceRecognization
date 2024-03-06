import os
import cv2
import face_recognition
import pickle

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

#link provided by firewall to storage
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facerecognition-42a2d-default-rtdb.firebaseio.com/",
    'storageBucket':"facerecognition-42a2d.appspot.com"
})


# importing Student images and ID's into the list
folderPath='StudentImages'
stuImgPathList=os.listdir(folderPath)
stuImgList=[]
stuIdList=[]

for path in stuImgPathList:
    stuImgList.append(cv2.imread(os.path.join(folderPath,path)))
    stuIdList.append(os.path.splitext(path)[0])
    print(path)
    print(os.path.splitext(path)[0])
#
    #Adding images to the database
    filename=f'{folderPath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(filename)
    blob.upload_from_filename(filename)




#Decoding the student Images into decoded value

def findEncode(imageList):
    encodedList=[]
    for img in imageList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)         #cv2 use BGR but face_recognition use RGB we need to conver it
        encode=face_recognition.face_encodings(img)[0]      #Storing the encoded value
        encodedList.append(encode)                          #appending in the list
    return encodedList

print("Encoding Started...")
encodedListKnown=findEncode(stuImgList)
encodedListKnownWithID=[encodedListKnown,stuIdList]         #storing the encoded values with the respective student ID
#print(encodedListKnown)
print("Encoding Complete!!")

file=open("StudentEncodeFile.p",'wb')                              #wb->opens the file in binary format for writing
pickle.dump(encodedListKnownWithID,file)                    #Saving or Dumping in the pickle File
file.close()
print("Encoding File Saved!!")