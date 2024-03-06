import os
import pickle

import dlib
import numpy as np
import cv2      #popular computer vision and image processing library - various tools and functions for working with images and videos.
import face_recognition
import cvzone

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

import PartialFace
#link provided by firewall for data base and storage bucket
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facerecognition-42a2d-default-rtdb.firebaseio.com/",
    'storageBucket':"facerecognition-42a2d.appspot.com"
})


#capture video from webcam
cap=cv2.VideoCapture(0)     #cap. This object is used to capture video frames from a camera
# cap=cv2.VideoCapture(1)     #cap. This object is used to capture video frames from a camera
cap.set(3,640)      #sets the width of the video capture frame
cap.set(4,480)      #sets the height of the video capture frame
imgBackground=cv2.imread('Resources/background.png')     #reding the background img

#importing Mode images into the list
folderModePath='Resources/Modes'        #assigns the directory path
modePathList=os.listdir(folderModePath)      #obtain a list of filenames in the directory
imgModeList=[]
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))       #join() to create the full path to the current image
#print(len(imgModeList))


#load the encoded file
print("Loding Encoded FIle")
file=open('StudentEncodeFile.p','rb')              #Opening the dumped pickle File
encodedListKnownWithID= pickle.load(file)   #Storing the values in the list
file.close()
encodedListKnown,stuIdList=encodedListKnownWithID   #seperately storint the ID and Encoded values

facFile=open('FacultyEncodeFile.p','rb')              #Opening the dumped pickle File
facEncodedListKnownWithID= pickle.load(facFile)   #Storing the values in the list
facFile.close()
facEncodedListKnown,facIdList=facEncodedListKnownWithID   #seperately storint the ID and Encoded values

#print(encodedListKnownWithID)
print("Encoded FIle Loaded")

counter=0       #to ensure the details has been downloaded to the data base only once
id=-1           #will be used to store the student ID to the Future purpose

while True:
    success,img=cap.read()      #read the video through the camera - store it in the img variable - success is a bolean value if img readed true else false;
    #cv2.imshow("Webcam",img)      #show the img with the respective title

    now = datetime.now()                    #checking the time table
    current_time = now.strftime("%H:%M:%S")           #ct->current_time
    # print("Current Time =", current_time)

    # BREAK CHECKING
    if (current_time>="10:40:00" and current_time<="10:50:00") or (current_time>="12:30:00" and current_time<="13:30:00"):
        print("break")
        continue

    imgS = cv2.resize(img,(0,0),None,0.25,0.25)      #Scalling the the web-cam image into 1/4th of its size
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)                    #changing the color



    faceCurFrame=face_recognition.face_locations(img)      #gives the pirticular face position in the image
    # print("faceFrame ",faceCurFrame)
    encodeCurFrame= face_recognition.face_encodings(img,faceCurFrame)      #Encode the pirticular portion of the img

    imgBackground[162:162+480, 55:55+640] =img     #overlayingthe background img with web-cam img
    imgBackground[44:44+633, 808:808+414] = imgModeList[2]

    #Faculty Check
    # for encodedFace, faceLoc in zip(encodeCurFrame,faceCurFrame):       #store the value of encodeCurFrame in encodedFace & faceCurFrame in faceLoc
    #     matches= face_recognition.compare_faces(facEncodedListKnown,encodedFace)   #check if it match or not
    #     faceDis= face_recognition.face_distance(facEncodedListKnown,encodedFace)   #Given the possible min value
    #     # print("matches",matches)
    #     # print("faceDis",faceDis)
    #
    #     matchIndex=np.argmin(faceDis)           #gives the min distance index
    #
    #     if matches[matchIndex]:
    #         print("Faculty Found")
    #         continue
    for encodedFace, faceLoc in zip(encodeCurFrame,faceCurFrame):       #store the value of encodeCurFrame in encodedFace & faceCurFrame in faceLoc
        matches= face_recognition.compare_faces(encodedListKnown,encodedFace)   #check if it match or not
        faceDis= face_recognition.face_distance(encodedListKnown,encodedFace)   #Given the possible min value
        # print("matches",matches)
        # print("faceDis",faceDis)

        matchIndex=np.argmin(faceDis)           #gives the min distance index
        maxMatchDist=np.max(faceDis)
        maxMatchDist=float(maxMatchDist * 10)
        threshold = 0.45

        if matches[matchIndex] and faceDis[matchIndex] <= threshold:
            # print("Known Face Detected")
            # print(stuIdList[matchIndex])
            y1,x2,y2,x1=faceLoc                     #to get an rectangle on the face - default values
            y1, x2, y2, x1 = y1, x2, y2, x1
            # y1, x2, y2, x1 =y1*4,x2*4,y2*4,x1*4     #in scaling we reducing the img sizeby 4 so now multiple by 4
            bbox=55+x1, 162+y1,x2-x1,y2-y1          #rectangle bound start from dist bbound->boundingBox
            imgBackground=cvzone.cornerRect(imgBackground,bbox,rt=0)    #assigning the rectangle to the existing image

            id=stuIdList[matchIndex]
            if counter==0:      #if it is a first Frame then change the counter into 1
                counter=1
        else:
            PartialFace.partilStudentCheck(img)
            continue

        """# INVALID FACES
        else:
            if maxMatchDist>=7.5:
                print("INVALID FACE")

                studentInfo = db.reference(f'Students/{id}').get()
                ref = db.reference(f'Students/{id}')

                # Uploading the student image in the firebase storage
                imageName = now.strftime("%Y-%m-%d %H:%M:%S")
                filename = f"UnusualSeekedStudents/{imageName}.jpg"  # path to store the img in database storage
                # Upload the current image to Firebase Storage
                bucket = storage.bucket()
                blob = bucket.blob(filename)
                _, img_encoded = cv2.imencode(".jpg", img)  # Encode the image as JPEG
                blob.upload_from_string(img_encoded.tobytes(), content_type="image/jpeg")
                print("Unusual images added to the data base!")"""

    if counter!=0:
        if counter==1:              #if it is a first frame then fetch the details of the student info with the respective ID
            studentInfo=db.reference(f'Students/{id}').get()
            ref = db.reference(f'Students/{id}')
            # print(studentInfo)

            #updating the last_seeked
            datetimeObject=datetime.strptime(studentInfo['last_seeked'],"%Y-%m-%d %H:%M:%S")
            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
            ref.child('last_seeked').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # now = datetime.now()
            # current_time = now.strftime("%H:%M:%S")
            # print("Current Time =", current_time)

            if secondsElapsed>=30:
                #updating the values in the Seeked students DB
                keyName = str(studentInfo['name'])+"_"+now.strftime("%Y-%m-%d %H:%M:%S") #because the key name should be different current_time mentioned above
                seekedRef = db.reference('SeekedStudents')  # creating the directory reference in the DB to store students who seeked
                data={
                    keyName:{
                        "regno":id,
                        "name": studentInfo['name'],
                        "major": studentInfo['major'],
                        "section": studentInfo['section'],
                        "year": studentInfo['year'],
                        "last_seeked": current_time
                    }
                }
                for key, value in data.items():
                    seekedRef.child(key).set(value)

                #Uploading the student image in the firebase storage
                imageName=keyName    #giving the unique image name
                filename = f"SeekedStudents/{imageName}.jpg"        #path to store the img in database storage
                    # Upload the current image to Firebase Storage
                bucket = storage.bucket()
                blob = bucket.blob(filename)
                _,img_encoded = cv2.imencode(".jpg", img)  # Encode the image as JPEG
                blob.upload_from_string(img_encoded.tobytes(), content_type="image/jpeg")
                print("Data and images added to the data base!")

                # updating the total numberOf_time_seekeds
                studentInfo['numberOf_time_seeked'] += 1
                ref.child('numberOf_time_seeked').set(studentInfo['numberOf_time_seeked'])
                print(studentInfo)
            else:
                print("Already Marked!!")

        counter = 0             #setting back to empty and zero to fetch new student
        studentInfo = []

    cv2.imshow("Face Recognition",imgBackground)
    cv2.waitKey(1)      #waits for 1 millisecond


