import face_recognition as fr
import cv2
import numpy as np
import os
import random
import pickle

MODEL_PATH = './model/celebrity_model.pkl'

# Load and encode training images from subfolders
def load_known_faces(path="./train/"):
    print('Training model. Please wait...')
    known_names = []
    known_name_encodings = []

    # Traverse through each folder and load images
    for celebrity_name in os.listdir(path):
        celebrity_folder = os.path.join(path, celebrity_name)
        print(celebrity_name)

        # Ensure that the item is a directory
        if os.path.isdir(celebrity_folder):
            for img_name in os.listdir(celebrity_folder):
                img_path = os.path.join(celebrity_folder, img_name)
                print(img_path)

                # Load the image and encode it
                try:
                    image = fr.load_image_file(img_path)
                    encodings = fr.face_encodings(image)

                    # Ensure that the image contains a face encoding
                    if len(encodings) > 0:
                        encoding = encodings[0]
                        known_name_encodings.append(encoding)
                        # Use the folder name (celebrity name) for labeling
                        known_names.append(celebrity_name.capitalize())
                except Exception as e:
                    print(f"Error processing image {img_name}: {e}")

    # Save the model to a file for future use
    save_model(known_name_encodings, known_names)
    return known_name_encodings, known_names

# Ensure the model directory exists before saving the model
if not os.path.exists('./model'):
    os.makedirs('./model')

# Save the trained model to a file
def save_model(encodings, names):
    print('Saving model to disk...')
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump((encodings, names), f)

# Load the trained model from a file
def load_model():
    if os.path.exists(MODEL_PATH):
        print('Loading model from disk...')
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    return None, None

# Initialize the model (load from file if available, otherwise train)
known_name_encodings, known_names = load_model()

if not known_name_encodings or not known_names:
    known_name_encodings, known_names = load_known_faces()

# Function to recognize faces from a test image
def recognize_faces(test_image_path):
    image = cv2.imread(test_image_path)

    face_locations = fr.face_locations(image)
    face_encodings = fr.face_encodings(image, face_locations)

    person_name = "Unknown"
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = fr.compare_faces(known_name_encodings, face_encoding)
        face_distances = fr.face_distance(known_name_encodings, face_encoding)
        best_match = np.argmin(face_distances)

        if matches[best_match]:
            person_name = known_names[best_match]

        # Draw rectangle around the face and label it
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(image, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, person_name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Save the output image with a random filename
    output_filename = f"img{random.randint(1000, 9999)}.jpg"
    output_path = os.path.join('./outputs', output_filename)
    cv2.imwrite(output_path, image)

    return output_path, person_name
