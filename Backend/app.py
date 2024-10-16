from flask import Flask, request, send_from_directory, jsonify
import os
import time
import random
from celebrity_recognition_service import recognize_faces
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Folder to store uploaded images
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create directories if they don't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists('./outputs'):
    os.makedirs('./outputs')

if not os.path.exists('./model'):
    os.makedirs('./model')

@app.route('/outputs/<path:filename>', methods=['GET'])
def serve_image(filename):
    # Use send_from_directory to serve the image file
    return send_from_directory('./outputs', filename)

# Helper function to get file extension
def get_file_extension(filename):
    return os.path.splitext(filename)[1]

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Get the file extension from the original file
    file_extension = get_file_extension(file.filename)

    # Refactor the file name to the current epoch time with original extension
    epoch_time = int(time.time())
    filename = f"{epoch_time}{file_extension}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    return jsonify({"image_path": file_path}), 200

@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.json
    img_path = data.get('imgPath')

    if not os.path.exists(img_path):
        return jsonify({'error': 'Image file not found'}), 400

    try:
        output_img_path, recognized_person = recognize_faces(img_path)
        response = {
            'imgPath': output_img_path,
            'person': recognized_person
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)
