from datetime import datetime
import os
import pickle
import numpy as np
import cv2
import face_recognition
import dlib

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

def is_obscured(landmarks):
    if not landmarks:
        # No landmarks detected
        return True


    # Check if left eye and right eye landmarks are detected
    if 'left_eye' in landmarks[0] and 'right_eye' in landmarks[0]:
        left_eye = landmarks[0]['left_eye']
        right_eye = landmarks[0]['right_eye']

        if not left_eye or not right_eye:
            return True
    # Check if top lip and bottom lip landmarks are detected
    if 'top_lip' in landmarks[0] and 'bottom_lip' in landmarks[0]:
        top_lip = landmarks[0]['top_lip']
        bottom_lip = landmarks[0]['bottom_lip']

        if not top_lip or not bottom_lip:
            return True
    # Check if nose bridge, nose tip, left cheek, right cheek, and forehead landmarks are detected
    if 'nose_bridge' in landmarks[0] and 'nose_tip' in landmarks[0] and 'left_cheek' in landmarks[
        0] and 'right_cheek' in landmarks[0] and 'forehead' in landmarks[0]:
        nose_bridge = landmarks[0]['nose_bridge']
        nose_tip = landmarks[0]['nose_tip']
        left_cheek = landmarks[0]['left_cheek']
        right_cheek = landmarks[0]['right_cheek']
        forehead = landmarks[0]['forehead']
        # Add conditions to check for obscured nose, cheeks, or forehead as needed
        if not nose_bridge or not nose_tip:
            return True
        if not left_cheek or not right_cheek:
            return True
        if not forehead:
            return True
    return False

def partilStudentCheck(partialImage):
    # Load the face detection model from dlib
    detector = dlib.get_frontal_face_detector()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # Use the provided image
    img_rgb = cv2.cvtColor(partialImage, cv2.COLOR_BGR2RGB)
    # Detect all faces in the image
    faces = detector(img_rgb)

    for face in faces:
        # Get the coordinates of the face bounding box
        top, right, bottom, left = (face.top(), face.right(), face.bottom(), face.left())
        # Crop the face from the image
        face_img = partialImage[top:bottom, left:right]
        # Convert the cropped face image to RGB
        face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        # Detect landmarks on the cropped face
        landmarks = face_recognition.face_landmarks(face_img_rgb)

        # Check if facial landmarks indicate obscured face
        if is_obscured(landmarks):
            print("INVALID FACE ", current_time)
            studentInfo = db.reference(f'Students/{id}').get()
            ref = db.reference(f'Students/{id}')

            # Uploading the student image in the firebase storage
            imageName = now.strftime("%Y-%m-%d %H:%M:%S")
            filename = f"UnusualSeekedStudentsCHECK/{imageName}.jpg"  # path to store the img in database storage

            try:
                # Upload the current image to Firebase Storage
                bucket = storage.bucket()
                blob = bucket.blob(filename)
                _, img_encoded = cv2.imencode(".jpg", partialImage)  # Encode the image as JPEG
                blob.upload_from_string(img_encoded.tobytes(), content_type="image/jpeg")
                print("Unusual image added to the database!")
            except Exception as e:
                print(f"Error uploading image to Firebase Storage: {str(e)}")
        else:
            print("VALID FACE")