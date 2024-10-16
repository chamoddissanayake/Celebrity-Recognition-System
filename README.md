
# Celebrity Recognition System


The Celebrity Recognition System is a Flask-based web application designed to identify faces in images. Users can upload photos, which are processed to recognize and label celebrities based on a pre-trained model. The system utilizes advanced face recognition techniques, providing immediate feedback with labeled images. With a user-friendly interface and support for image uploads, it seamlessly combines cutting-edge technology with accessibility, making it an engaging tool for fans and developers alike.
## Run Locally

Install Python 3.10.0


  https://www.python.org/downloads/release/python-3100/

Install Node 21.6.2


  https://nodejs.org/en/blog/release/v21.6.2


Clone the project

```bash
  git clone https://github.com/chamoddissanayake/Celebrity-Recognition-System.git
```

Go to Frontend Folder

```bash
  Frontend > celebrity-recognition
```

Install dependencies

```bash
  npm install
```

Start the Frontend

```bash
  npm start
```

Go to Frontend Web App

```bash
  http://localhost:3000/
```

Go to Backend Folder

```bash
  Backend >
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the Backend

```bash
  python app.py
```
## Tech Stack

**Backend Framework:** Flask

**Face Recognition Library:** Face_recognition

**Image Processing:** OpenCV (cv2)

**Programming Language:** Python

**Web Server:** Flask development server

**Frontend:** React
## Usage/Examples

POST Method

```bash
http://localhost:5008/recognize
```

Request
```javascript
{"imgPath": "./test/test2.jpg"}
```
Response
```javascript
{
    "imgPath": "./outputs\\img5830.jpg",
    "person": "Elon Musk"
}
```