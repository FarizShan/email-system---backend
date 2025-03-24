# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import numpy as np
# import cv2
# import os

# app = Flask(__name__)
# CORS(app)  # Allow all origins (for development)

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/register', methods=['POST'])
# def register():
#     try:
#         # Check if required fields are present in the request
#         if 'email' not in request.form or 'password' not in request.form:
#             return jsonify({"error": "Missing email or password"}), 400
        
#         if 'image' not in request.files:
#             return jsonify({"error": "No image provided"}), 400

#         # Extract form data
#         email = request.form['email']
#         password = request.form['password']
#         image_file = request.files['image']  # Get the uploaded image Blob

#         # Validate the image file
#         if image_file.filename == '':
#             return jsonify({"error": "No image selected"}), 400

#         # Read the image as bytes and decode it with OpenCV
#         image_bytes = image_file.read()
#         nparr = np.frombuffer(image_bytes, np.uint8)
#         img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#         if img is None:
#             return jsonify({"error": "Invalid image format"}), 400

#         # Save the image
#         img_path = os.path.join(UPLOAD_FOLDER, 'face.jpg')
#         cv2.imwrite(img_path, img)

#         return jsonify({
#             "status": "success",  # Match frontend expectation
#             "message": "Registration successful",
#             "image_path": img_path
#         })

#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import face_recognition
import sqlite3
import os
import uuid
import smtplib

app = Flask(__name__)
# CORS(app)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id TEXT PRIMARY KEY, email TEXT UNIQUE, app_password TEXT, image_path TEXT)''')
    conn.commit()
    conn.close()

init_db()

# @app.route('/register', methods=['POST'])
# def register():
#     try:
#         if 'email' not in request.form or 'app_password' not in request.form:
#             return jsonify({"error": "Missing email or app password"}), 400
#         if 'image' not in request.files:
#             return jsonify({"error": "No image provided"}), 400

#         email = request.form['email']
#         app_password = request.form['app_password']  # Plain text
#         image_file = request.files['image']

#         image_bytes = image_file.read()
#         nparr = np.frombuffer(image_bytes, np.uint8)
#         img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#         if img is None:
#             return jsonify({"error": "Invalid image format"}), 400

#         img_filename = f"{uuid.uuid4().hex}.jpg"
#         img_path = os.path.join(UPLOAD_FOLDER, img_filename)
#         cv2.imwrite(img_path, img)

#         user_id = str(uuid.uuid4())
#         conn = sqlite3.connect('users.db')
#         c = conn.cursor()
#         c.execute("INSERT INTO users (id, email, app_password, image_path) VALUES (?, ?, ?, ?)",
#                   (user_id, email, app_password, img_path))  # Store as plain text
#         conn.commit()
#         conn.close()

#         return jsonify({"status": "success", "message": "Registration successful", "image_path": img_path})

#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"error": str(e)}), 500

@app.route('/register', methods=['POST'])
def register():
    try:
        if 'email' not in request.form or 'password' not in request.form:  # Adjusted to match frontend
            return jsonify({"error": "Missing email or password"}), 400
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        email = request.form['email']
        app_password = request.form['password']  # Changed to 'password' to match frontend
        image_file = request.files['image']

        # Process the image
        image_bytes = image_file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Invalid image format"}), 400

        # Save the image
        img_filename = f"{uuid.uuid4().hex}.jpg"
        img_path = os.path.join(UPLOAD_FOLDER, img_filename)
        cv2.imwrite(img_path, img)

        # Store user in database
        user_id = str(uuid.uuid4())
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (id, email, app_password, image_path) VALUES (?, ?, ?, ?)",
                  (user_id, email, app_password, img_path))
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": "Registration successful", "image_path": img_path})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        image_file = request.files['image']
        image_bytes = image_file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        login_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if login_img is None:
            return jsonify({"error": "Invalid image format"}), 400

        login_img_rgb = cv2.cvtColor(login_img, cv2.COLOR_BGR2RGB)
        login_face_encodings = face_recognition.face_encodings(login_img_rgb)

        if not login_face_encodings:
            return jsonify({"error": "No face detected in the image"}), 400

        login_face_encoding = login_face_encodings[0]

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id, email, app_password, image_path FROM users")
        users = c.fetchall()
        conn.close()

        for user in users:
            user_id, email, stored_app_password, img_path = user
            stored_img = cv2.imread(img_path)
            if stored_img is None:
                continue

            stored_img_rgb = cv2.cvtColor(stored_img, cv2.COLOR_BGR2RGB)
            stored_face_encodings = face_recognition.face_encodings(stored_img_rgb)

            if not stored_face_encodings:
                continue

            stored_face_encoding = stored_face_encodings[0]
            match = face_recognition.compare_faces([stored_face_encoding], login_face_encoding, tolerance=0.6)

            if match[0]:
                try:
                    # Ensure stored_app_password is a string
                    if isinstance(stored_app_password, bytes):
                        stored_app_password = stored_app_password.decode('utf-8')  # Convert bytes to string if needed
                    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                    smtp_server.starttls()
                    smtp_server.login(email, stored_app_password)
                    smtp_server.quit()
                    return jsonify({"status": "success", "message": "Login successful", "email": email})
                except smtplib.SMTPAuthenticationError:
                    return jsonify({"error": "Gmail authentication failed"}), 401
                except Exception as e:
                    print(f"Gmail login error: {str(e)}")
                    return jsonify({"error": f"Gmail login error: {str(e)}"}), 500

        return jsonify({"error": "Face not recognized"}), 401

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)