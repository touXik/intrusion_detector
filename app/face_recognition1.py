import face_recognition
import os 
import cv2
import numpy as np

def load_known_faces(model_dir="models"):
    known_encodings = []
    known_names = []

    for name in os.listdir(model_dir):
        person_dir = os.path.join(model_dir,name)
        if not os.path.isdir(person_dir):
            continue
        
        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir,img_name)
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)

            if encodings : 
                known_encodings.append(encodings[0])
                known_names.append(name)
    return known_encodings, known_names

def recognize_faces_in_frame(frame,known_encodings,known_names):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    recognized = []

    for encoding, location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        name = "Inconnu"

        if True in matches:
            best_match_index = np.argmin(face_recognition.face_distance(known_encodings, encoding))
            name = known_names[best_match_index]
        
        recognized.append((name, location))

    return recognized



