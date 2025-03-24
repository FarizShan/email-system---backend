# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# app = Flask(__name__)
# CORS(app)

# # Configure Gemini API
# genai.configure(api_key="AIzaSyAbBejxnh7uT8Xqp-SlzSN5O2z5pfzMe-k")

# def send_email(receiver_email, subject, content, cc_emails):
#     sender_email = "draaft001@gmail.com"
#     password = "hxrvnhczikjuwlva"

#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Cc"] = cc_emails
#     message["Subject"] = subject
#     message.attach(MIMEText(content, "plain"))

#     all_recipients = [receiver_email] + cc_emails.split(",")
#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(sender_email, password)
#             server.sendmail(sender_email, all_recipients, message.as_string())
#         return {"status": "success", "message": "Email sent successfully!"}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# @app.route("/generate-email", methods=["POST"])
# def generate_email():
#     data = request.json
#     user_prompt = data.get("user_prompt", "")
#     system_prompt = """
#     Please write an email in the style of the user given a prompt and the sample emails below. 
#     It should be formal, keep the email content within 50 words, 
#     just express what the user says in the prompt. Sign t he email as Fariz.
#     """
#     try:
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         chat = model.start_chat(history=[{"role": "user", "parts": system_prompt}])
#         response = chat.send_message(user_prompt)
#         return jsonify({"status": "success", "email_content": response.text})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})

# @app.route("/send-email", methods=["POST"])
# def send_email_route():
#     data = request.json
#     receiver_email = data.get("receiver_email")
#     subject = data.get("subject")
#     content = data.get("content")
#     cc_emails = data.get("cc_emails", "")
#     result = send_email(receiver_email, subject, content, cc_emails)
#     return jsonify(result)

# if __name__ == "__main__":
#     app.run(debug=True)



#latest working code

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# app = Flask(__name__)
# CORS(app)

# genai.configure(api_key="AIzaSyAbBejxnh7uT8Xqp-SlzSN5O2z5pfzMe-k")

# @app.route('/generate-email', methods=['POST'])
# def generate_email():
#     data = request.json
#     user_prompt = data["prompt"]
#     system_prompt = """
#     Write a professional email in 100 words.Maintain a formal and concise tone.
#     Sign the email as fariz.
#     """
    
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     chat = model.start_chat(history=[{"role": "user", "parts": system_prompt}])
#     response = chat.send_message(user_prompt)
    
#     return jsonify({"email": response.text})

# @app.route('/send-email', methods=['POST'])
# def send_email():
#     data = request.json
#     receiver_email = data["receiverEmail"]
#     subject = data["subject"]
#     content = data["content"]
#     cc_emails = data.get("ccEmails", [])
    
#     sender_email = "draaft001@gmail.com"
#     password = "hxrvnhczikjuwlva"

#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Cc"] = ", ".join(cc_emails)
#     message["Subject"] = subject
#     message.attach(MIMEText(content, "plain"))
    
#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(sender_email, password)
#             server.sendmail(sender_email, [receiver_email] + cc_emails, message.as_string())
#         return jsonify({"message": "Email sent successfully!"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(port=5000)




#another working version

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import re  # 📝 Added for response parsing

# app = Flask(__name__)
# CORS(app)

# genai.configure(api_key="AIzaSyAbBejxnh7uT8Xqp-SlzSN5O2z5pfzMe-k")

# @app.route('/generate-email', methods=['POST'])
# def generate_email():
#     data = request.json
#     user_prompt = data["prompt"]
#     system_prompt = """
#     📝 Generate a professional email with subject and body based on the user's description.
#     Follow this format exactly:
    
#     Subject: [Generated subject here]
    
#     Body: [Generated email body here]
    
#     - Keep subject under 10 words
#     - Maintain formal tone
#     - Body should be 50-100 words and provide proper indentation and spacing
#     - Sign off as "fariz"
#     """
    
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     chat = model.start_chat(history=[])
#     # 📝 Combined prompt for better context understanding
#     full_prompt = f"{system_prompt}\n\nUser request: {user_prompt}"
#     response = chat.send_message(full_prompt)
    
#     # 📝 Parse response into subject and body
#     try:
#         # Split response into subject and body sections
#         parts = re.split(r'Subject:|Body:', response.text, flags=re.IGNORECASE)
#         subject = parts[1].split('\n')[0].strip()
#         body = ' '.join(parts[2].strip().split('\n'))
#     except Exception as e:
#         # Fallback if parsing fails
#         subject = "Important Message"
#         body = response.text
    
#     return jsonify({
#         "email": body,
#         "subject": subject  # 📝 Added subject to response
#     })

# # 📝 The send-email route remains unchanged from original
# @app.route('/send-email', methods=['POST'])
# def send_email():
#     data = request.json
#     receiver_email = data["receiverEmail"]
#     subject = data["subject"]
#     content = data["content"]
#     cc_emails = data.get("ccEmails", [])
    
#     sender_email = "email@gmail.com"
#     password = "email pass"

#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Cc"] = ", ".join(cc_emails)
#     message["Subject"] = subject
#     message.attach(MIMEText(content, "plain"))
    
#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(sender_email, password)
#             server.sendmail(sender_email, [receiver_email] + cc_emails, message.as_string())
#         return jsonify({"message": "Email sent successfully!"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(port=5000)




#working code

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# app = Flask(__name__)
# CORS(app)

# # Configure Google Generative AI with your API key
# genai.configure(api_key="AIzaSyAbBejxnh7uT8Xqp-SlzSN5O2z5pfzMe-k")

# @app.route('/generate-email', methods=['POST'])
# def generate_email():
#     data = request.json
#     user_prompt = data["prompt"]
#     system_prompt = """
#     📝 Generate a professional email with subject and body based on the user's description.
#     Follow this exact format (do not deviate):

#     Subject: [Generated subject here]

#     Body:
#     [Generated email body here with proper spacing]

#     - Keep subject under 10 words
#     - Maintain formal tone
#     - Body should be 50-100 words with proper indentation and line spacing after salutation and regards(before & after).
#     - Sign off as "fariz"
#     - Do not include extra text outside this structure
#     """
    
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     chat = model.start_chat(history=[])
#     full_prompt = f"{system_prompt}\n\nUser request: {user_prompt}"
#     response = chat.send_message(full_prompt)
    
#     # Parse response into subject and body
#     try:
#         # Split by lines and look for Subject and Body markers
#         lines = response.text.strip().split('\n')
#         subject = ""
#         body_lines = []
#         body_started = False
        
#         for line in lines:
#             if line.lower().startswith("subject:"):
#                 subject = line[len("Subject:"):].strip()
#             elif line.lower().startswith("body:"):
#                 body_started = True
#             elif body_started and line.strip():
#                 body_lines.append(line.strip())
        
#         body = '\n'.join(body_lines) if body_lines else response.text  # Fallback to full text if no body lines
        
#         if not subject or not body:
#             raise ValueError("Failed to parse subject or body from response")
#     except Exception as e:
#         # Fallback if parsing fails
#         print(f"Parsing error: {str(e)}, Raw response: {response.text}")
#         subject = "Important Message"
#         body = response.text
    
#     return jsonify({
#         "email": body,
#         "subject": subject
#     })

# @app.route('/send-email', methods=['POST'])
# def send_email():
#     data = request.json
#     receiver_email = data["receiverEmail"]
#     subject = data["subject"]
#     content = data["content"]
#     cc_emails = data.get("ccEmails", [])
    
#     sender_email = "draaft001@gmail.com"
#     password = "hxrvnhczikjuwlva"

#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Cc"] = ", ".join(cc_emails)
#     message["Subject"] = subject
#     message.attach(MIMEText(content, "plain"))
    
#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(sender_email, password)
#             server.sendmail(sender_email, [receiver_email] + cc_emails, message.as_string())
#         return jsonify({"message": "Email sent successfully!"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(port=5000)


#working code


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# app = Flask(__name__)
# CORS(app)

# # Configure Google Generative AI with your API key
# genai.configure(api_key="AIzaSyAbBejxnh7uT8Xqp-SlzSN5O2z5pfzMe-k")

# # Store chat sessions in memory (use a database for production)
# chat_sessions = {}

# # System prompt for email generation
# system_prompt = """
# 📝 Generate a professional email with subject and body based on the user's description.
# Follow this exact format (do not deviate):

# Subject: [Generated subject here]

# Body:
# [Generated email body here with proper spacing]

# - Keep subject under 10 words
# - Maintain formal tone
# - Body should be 50-100 words with proper indentation and line spacing after salutation and regards(before & after).
# - Sign off as "fariz"
# - Do not include extra text outside this structure
# """

# @app.route('/generate-email', methods=['POST'])
# def generate_email():
#     data = request.json
#     user_prompt = data["prompt"]
#     session_id = data.get("session_id", "default")  # Unique session ID from client

#     # Initialize or retrieve chat session
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     if session_id not in chat_sessions:
#         # Start a new chat with the system prompt as the first message
#         chat_sessions[session_id] = model.start_chat(history=[
#             {"role": "user", "parts": [system_prompt]},
#             {"role": "model", "parts": ["Understood, please provide your request."]}
#         ])
#     chat = chat_sessions[session_id]

#     # Send the user's prompt to the chat
#     response = chat.send_message(user_prompt)
    
#     # Parse response into subject and body
#     try:
#         lines = response.text.strip().split('\n')
#         subject = ""
#         body_lines = []
#         body_started = False
        
#         for line in lines:
#             if line.lower().startswith("subject:"):
#                 subject = line[len("Subject:"):].strip()
#             elif line.lower().startswith("body:"):
#                 body_started = True
#             elif body_started and line.strip():
#                 body_lines.append(line.strip())
        
#         body = '\n'.join(body_lines) if body_lines else response.text
        
#         if not subject or not body:
#             raise ValueError("Failed to parse subject or body from response")
#     except Exception as e:
#         print(f"Parsing error: {str(e)}, Raw response: {response.text}")
#         subject = "Important Message"
#         body = response.text
    
#     return jsonify({
#         "email": body,
#         "subject": subject,
#         "session_id": session_id  # Return session ID for client to reuse
#     })

# @app.route('/send-email', methods=['POST'])
# def send_email():
#     data = request.json
#     receiver_email = data["receiverEmail"]
#     subject = data["subject"]
#     content = data["content"]
#     cc_emails = data.get("ccEmails", [])
    
#     sender_email = "draaft001@gmail.com"
#     password = "hxrvnhczikjuwlva"

#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Cc"] = ", ".join(cc_emails)
#     message["Subject"] = subject
#     message.attach(MIMEText(content, "plain"))
    
#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(sender_email, password)
#             server.sendmail(sender_email, [receiver_email] + cc_emails, message.as_string())
#         return jsonify({"message": "Email sent successfully!"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(port=5000)


from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import face_recognition
import sqlite3
import os
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Hardcoded Google Generative AI API key (as requested, no environment variables)
GOOGLE_API_KEY = "AIzaSyAbBejxnh7uT8Xqp-SlzSN5O2z5pfzMe-k"

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# Store chat sessions in memory (use a database for production)
chat_sessions = {}

# System prompt for email generation
system_prompt = """
📝 Generate a professional email with subject and body based on the user's description.
Follow this exact format (do not deviate):

Subject: [Generated subject here]

Body:
[Generated email body here with proper spacing]

- Keep subject under 10 words
- Maintain formal tone
- Body should be 50-100 words with proper indentation and line spacing after salutation and regards(before & after).
- Sign off as "fariz"
- Do not include extra text outside this structure
"""

# Initialize SQLite database for user storage
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id TEXT PRIMARY KEY, email TEXT UNIQUE, app_password TEXT, image_path TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Authentication Endpoints
@app.route('/register', methods=['POST'])
def register():
    try:
        if 'email' not in request.form or 'app_password' not in request.form:
            return jsonify({"error": "Missing email or app password"}), 400
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        email = request.form['email']
        app_password = request.form['app_password']  # Plain text (consider hashing in production)
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
                  (user_id, email, app_password, img_path))  # Store as plain text (not secure)
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

        # Process the login image for facial recognition
        login_img_rgb = cv2.cvtColor(login_img, cv2.COLOR_BGR2RGB)
        login_face_encodings = face_recognition.face_encodings(login_img_rgb)

        if not login_face_encodings:
            return jsonify({"error": "No face detected in the image"}), 400

        login_face_encoding = login_face_encodings[0]

        # Retrieve all users from the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id, email, app_password, image_path FROM users")
        users = c.fetchall()
        conn.close()

        # Compare the login image with stored images
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
                        stored_app_password = stored_app_password.decode('utf-8')
                    # Verify Gmail credentials
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

# Email Generation and Sending Endpoints
@app.route('/generate-email', methods=['POST'])
def generate_email():
    data = request.json
    user_prompt = data["prompt"]
    session_id = data.get("session_id", "default")  # Unique session ID from client

    # Initialize or retrieve chat session
    model = genai.GenerativeModel("gemini-1.5-flash")
    if session_id not in chat_sessions:
        # Start a new chat with the system prompt as the first message
        chat_sessions[session_id] = model.start_chat(history=[
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["Understood, please provide your request."]}
        ])
    chat = chat_sessions[session_id]

    # Send the user's prompt to the chat
    response = chat.send_message(user_prompt)
    
    # Parse response into subject and body
    try:
        lines = response.text.strip().split('\n')
        subject = ""
        body_lines = []
        body_started = False
        
        for line in lines:
            if line.lower().startswith("subject:"):
                subject = line[len("Subject:"):].strip()
            elif line.lower().startswith("body:"):
                body_started = True
            elif body_started and line.strip():
                body_lines.append(line.strip())
        
        body = '\n'.join(body_lines) if body_lines else response.text
        
        if not subject or not body:
            raise ValueError("Failed to parse subject or body from response")
    except Exception as e:
        print(f"Parsing error: {str(e)}, Raw response: {response.text}")
        subject = "Important Message"
        body = response.text
    
    return jsonify({
        "email": body,
        "subject": subject,
        "session_id": session_id  # Return session ID for client to reuse
    })

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    sender_email = data.get("senderEmail")  # Sender's email from the request (set by frontend after login)
    receiver_email = data.get("receiverEmail")
    subject = data.get("subject")
    content = data.get("content")
    cc_emails = data.get("ccEmails", [])

    # Validate required fields
    if not sender_email:
        return jsonify({"error": "Sender email is required"}), 400
    if not receiver_email:
        return jsonify({"error": "Receiver email is required"}), 400
    if not subject:
        return jsonify({"error": "Subject is required"}), 400
    if not content:
        return jsonify({"error": "Content is required"}), 400

    # Retrieve the sender's app password from the database
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT app_password FROM users WHERE email = ?", (sender_email,))
        result = c.fetchone()
        conn.close()

        if not result:
            return jsonify({"error": "Sender email not found in database"}), 404

        sender_password = result[0]
        if isinstance(sender_password, bytes):
            sender_password = sender_password.decode('utf-8')

    except Exception as e:
        print(f"Error retrieving sender password: {str(e)}")
        return jsonify({"error": "Failed to retrieve sender credentials"}), 500

    # Send the email using the sender's Gmail credentials
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Cc"] = ", ".join(cc_emails)
    message["Subject"] = subject
    message.attach(MIMEText(content, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [receiver_email] + cc_emails, message.as_string())
        return jsonify({"message": "Email sent successfully!"})
    except smtplib.SMTPAuthenticationError:
        return jsonify({"error": "Gmail authentication failed for the sender's credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import numpy as np
# import cv2
# import face_recognition
# import sqlite3
# import os
# import uuid
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import google.generativeai as genai

# app = Flask(__name__)
# # Configure CORS with explicit settings
# CORS(app, resources={
#     r"/*": {
#         "origins": "http://localhost:3000",  # Allow only the frontend origin
#         "methods": ["GET", "POST", "OPTIONS"],  # Explicitly allow these methods
#         "allow_headers": ["Content-Type", "Authorization"],  # Allow these headers
#         "supports_credentials": False  # Disable credentials for simplicity
#     }
# })

# # Configuration
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Hardcoded Google Generative AI API key
# GOOGLE_API_KEY = "AIzaSyAbBejxnh7uT8Xqp-SlzSN5O2z5pfzMe-k"

# # Configure Google Generative AI
# genai.configure(api_key=GOOGLE_API_KEY)

# # Store chat sessions in memory (use a database for production)
# chat_sessions = {}

# # System prompt for email generation
# system_prompt = """
# 📝 Generate a professional email with subject and body based on the user's description.
# Follow this exact format (do not deviate):

# Subject: [Generated subject here]

# Body:
# [Generated email body here with proper spacing]

# - Keep subject under 10 words
# - Maintain formal tone
# - Body should be 50-100 words with proper indentation and line spacing after salutation and regards(before & after).
# - Sign off as "fariz"
# - Do not include extra text outside this structure
# """

# # Initialize SQLite database for user storage
# def init_db():
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS users
#                  (id TEXT PRIMARY KEY, email TEXT UNIQUE, app_password TEXT, image_path TEXT)''')
#     conn.commit()
#     conn.close()

# init_db()

# # Catch-all OPTIONS handler for all routes
# @app.before_request
# def handle_options():
#     if request.method == "OPTIONS":
#         print(f"Handling OPTIONS request for {request.path}")
#         return '', 200

# # Authentication Endpoints
# @app.route('/register', methods=['POST'])
# def register():
#     try:
#         if 'email' not in request.form or 'app_password' not in request.form:
#             return jsonify({"error": "Missing email or app password"}), 400
#         if 'image' not in request.files:
#             return jsonify({"error": "No image provided"}), 400

#         email = request.form['email']
#         app_password = request.form['app_password']
#         image_file = request.files['image']

#         # Process the image
#         image_bytes = image_file.read()
#         nparr = np.frombuffer(image_bytes, np.uint8)
#         img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#         if img is None:
#             return jsonify({"error": "Invalid image format"}), 400

#         # Save the image
#         img_filename = f"{uuid.uuid4().hex}.jpg"
#         img_path = os.path.join(UPLOAD_FOLDER, img_filename)
#         cv2.imwrite(img_path, img)

#         # Store user in database
#         user_id = str(uuid.uuid4())
#         conn = sqlite3.connect('users.db')
#         c = conn.cursor()
#         c.execute("INSERT INTO users (id, email, app_password, image_path) VALUES (?, ?, ?, ?)",
#                   (user_id, email, app_password, img_path))
#         conn.commit()
#         conn.close()

#         return jsonify({"status": "success", "message": "Registration successful", "image_path": img_path})

#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"error": str(e)}), 500

# @app.route('/login', methods=['POST'])
# def login():
#     try:
#         if 'image' not in request.files:
#             return jsonify({"error": "No image provided"}), 400

#         image_file = request.files['image']
#         image_bytes = image_file.read()
#         nparr = np.frombuffer(image_bytes, np.uint8)
#         login_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#         if login_img is None:
#             return jsonify({"error": "Invalid image format"}), 400

#         # Process the login image for facial recognition
#         login_img_rgb = cv2.cvtColor(login_img, cv2.COLOR_BGR2RGB)
#         login_face_encodings = face_recognition.face_encodings(login_img_rgb)

#         if not login_face_encodings:
#             return jsonify({"error": "No face detected in the image"}), 400

#         login_face_encoding = login_face_encodings[0]

#         # Retrieve all users from the database
#         conn = sqlite3.connect('users.db')
#         c = conn.cursor()
#         c.execute("SELECT id, email, app_password, image_path FROM users")
#         users = c.fetchall()
#         conn.close()

#         # Compare the login image with stored images
#         for user in users:
#             user_id, email, stored_app_password, img_path = user
#             stored_img = cv2.imread(img_path)
#             if stored_img is None:
#                 continue

#             stored_img_rgb = cv2.cvtColor(stored_img, cv2.COLOR_BGR2RGB)
#             stored_face_encodings = face_recognition.face_encodings(stored_img_rgb)

#             if not stored_face_encodings:
#                 continue

#             stored_face_encoding = stored_face_encodings[0]
#             match = face_recognition.compare_faces([stored_face_encoding], login_face_encoding, tolerance=0.6)

#             if match[0]:
#                 try:
#                     # Ensure stored_app_password is a string
#                     if isinstance(stored_app_password, bytes):
#                         stored_app_password = stored_app_password.decode('utf-8')
#                     # Verify Gmail credentials
#                     smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
#                     smtp_server.starttls()
#                     smtp_server.login(email, stored_app_password)
#                     smtp_server.quit()
#                     return jsonify({"status": "success", "message": "Login successful", "email": email})
#                 except smtplib.SMTPAuthenticationError:
#                     return jsonify({"error": "Gmail authentication failed"}), 401
#                 except Exception as e:
#                     print(f"Gmail login error: {str(e)}")
#                     return jsonify({"error": f"Gmail login error: {str(e)}"}), 500

#         return jsonify({"error": "Face not recognized"}), 401

#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"error": str(e)}), 500

# # Email Generation and Sending Endpoints
# @app.route('/generate-email', methods=['POST', 'OPTIONS'])
# def generate_email():
#     if request.method == 'OPTIONS':
#         print("Handling OPTIONS request for /generate-email (route-specific)")
#         return '', 200

#     data = request.json
#     user_prompt = data["prompt"]
#     session_id = data.get("session_id", "default")

#     # Initialize or retrieve chat session
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     if session_id not in chat_sessions:
#         chat_sessions[session_id] = model.start_chat(history=[
#             {"role": "user", "parts": [system_prompt]},
#             {"role": "model", "parts": ["Understood, please provide your request."]}
#         ])
#     chat = chat_sessions[session_id]

#     # Send the user's prompt to the chat
#     response = chat.send_message(user_prompt)
    
#     # Parse response into subject and body
#     try:
#         lines = response.text.strip().split('\n')
#         subject = ""
#         body_lines = []
#         body_started = False
        
#         for line in lines:
#             if line.lower().startswith("subject:"):
#                 subject = line[len("Subject:"):].strip()
#             elif line.lower().startswith("body:"):
#                 body_started = True
#             elif body_started and line.strip():
#                 body_lines.append(line.strip())
        
#         body = '\n'.join(body_lines) if body_lines else response.text
        
#         if not subject or not body:
#             raise ValueError("Failed to parse subject or body from response")
#     except Exception as e:
#         print(f"Parsing error: {str(e)}, Raw response: {response.text}")
#         subject = "Important Message"
#         body = response.text
    
#     return jsonify({
#         "email": body,
#         "subject": subject,
#         "session_id": session_id
#     })

# @app.route('/send-email', methods=['POST', 'OPTIONS'])
# def send_email():
#     if request.method == 'OPTIONS':
#         print("Handling OPTIONS request for /send-email (route-specific)")
#         return '', 200

#     data = request.json
#     sender_email = data.get("senderEmail")
#     receiver_email = data.get("receiverEmail")
#     subject = data.get("subject")
#     content = data.get("content")
#     cc_emails = data.get("ccEmails", [])

#     # Validate required fields
#     if not sender_email:
#         return jsonify({"error": "Sender email is required"}), 400
#     if not receiver_email:
#         return jsonify({"error": "Receiver email is required"}), 400
#     if not subject:
#         return jsonify({"error": "Subject is required"}), 400
#     if not content:
#         return jsonify({"error": "Content is required"}), 400

#     # Retrieve the sender's app password from the database
#     try:
#         conn = sqlite3.connect('users.db')
#         c = conn.cursor()
#         c.execute("SELECT app_password FROM users WHERE email = ?", (sender_email,))
#         result = c.fetchone()
#         conn.close()

#         if not result:
#             return jsonify({"error": "Sender email not found in database"}), 404

#         sender_password = result[0]
#         if isinstance(sender_password, bytes):
#             sender_password = sender_password.decode('utf-8')

#     except Exception as e:
#         print(f"Error retrieving sender password: {str(e)}")
#         return jsonify({"error": "Failed to retrieve sender credentials"}), 500

#     # Send the email using the sender's Gmail credentials
#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Cc"] = ", ".join(cc_emails)
#     message["Subject"] = subject
#     message.attach(MIMEText(content, "plain"))

#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, [receiver_email] + cc_emails, message.as_string())
#         return jsonify({"message": "Email sent successfully!"})
#     except smtplib.SMTPAuthenticationError:
#         return jsonify({"error": "Gmail authentication failed for the sender's credentials"}), 401
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
