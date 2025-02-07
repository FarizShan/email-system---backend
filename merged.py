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


from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyAbBejxnh7uT8Xqp-SlzSN5O2z5pfzMe-k")

@app.route('/generate-email', methods=['POST'])
def generate_email():
    data = request.json
    user_prompt = data["prompt"]
    system_prompt = """
    Write a professional email in 100 words.Maintain a formal and concise tone.
    Sign the email as fariz.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=[{"role": "user", "parts": system_prompt}])
    response = chat.send_message(user_prompt)
    
    return jsonify({"email": response.text})

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    receiver_email = data["receiverEmail"]
    subject = data["subject"]
    content = data["content"]
    cc_emails = data.get("ccEmails", [])
    
    sender_email = "draaft001@gmail.com"
    password = "hxrvnhczikjuwlva"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Cc"] = ", ".join(cc_emails)
    message["Subject"] = subject
    message.attach(MIMEText(content, "plain"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, [receiver_email] + cc_emails, message.as_string())
        return jsonify({"message": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
