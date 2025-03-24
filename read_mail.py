# from flask import Flask, jsonify
# from flask_cors import CORS
# import imaplib
# import email
# from email.header import decode_header

# app = Flask(__name__)
# CORS(app)  # Enable CORS

# # Email credentials (replace with your credentials or use environment variables)
# IMAP_SERVER = "imap.gmail.com"
# EMAIL_ACCOUNT = "draaft001@gmail.com"
# EMAIL_PASSWORD = "hxrvnhczikjuwlva"

# def fetch_emails():
#     try:
#         # Connect to the server
#         mail = imaplib.IMAP4_SSL(IMAP_SERVER)

#         # Login to your account
#         mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

#         # Select the mailbox you want to use (INBOX in this case)
#         mail.select("inbox")

#         # Search for all emails
#         status, messages = mail.search(None, "ALL")

#         # List to store email data
#         emails = []

#         # Convert messages to a list of email IDs
#         email_ids = messages[0].split()

#         for email_id in email_ids:
#             # Fetch the email by ID
#             res, msg = mail.fetch(email_id, "(RFC822)")
#             for response in msg:
#                 if isinstance(response, tuple):
#                     # Parse the raw email bytes
#                     msg = email.message_from_bytes(response[1])
#                     # Decode the email subject
#                     subject, encoding = decode_header(msg["Subject"])[0]
#                     if isinstance(subject, bytes):
#                         # Decode bytes to string
#                         subject = subject.decode(encoding if encoding else "utf-8")
#                     # Decode email sender
#                     from_ = msg.get("From")
#                     # Decode the date
#                     date = msg.get("Date")
#                     # Extract the email body
#                     if msg.is_multipart():
#                         for part in msg.walk():
#                             if part.get_content_type() == "text/plain":
#                                 body = part.get_payload(decode=True).decode()
#                                 break
#                     else:
#                         body = msg.get_payload(decode=True).decode()
                    
#                     # Append the email data to the list
#                     emails.append({
#                         "id": email_id.decode(),
#                         "from": from_,
#                         "subject": subject,
#                         "snippet": body[:100],  # Show the first 100 characters
#                         "date": date
#                     })

#         # Close the connection and logout
#         mail.close()
#         mail.logout()

#         return emails
#     except Exception as e:
#         print("Error fetching emails:", e)
#         return []

# @app.route('/get-emails', methods=['GET'])
# def get_emails():
#     emails = fetch_emails()
#     return jsonify(emails)

# if __name__ == '__main__':
#     app.run(port=5001, debug=True)



#### latest working

# from flask import Flask, jsonify
# from flask_cors import CORS
# import imaplib
# import email
# from email.header import decode_header
# import os

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend access

# # Email credentials (Use environment variables for security)
# IMAP_SERVER = "imap.gmail.com"
# EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT", "draaft001@gmail.com")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "hxrvnhczikjuwlva")

# def fetch_emails(folder_name):
#     """Fetch emails from a specific folder (Inbox or Spam)."""
#     try:
#         # Connect to the IMAP server
#         mail = imaplib.IMAP4_SSL(IMAP_SERVER)
#         mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        
#         # Select the folder (Inbox, Spam, or Junk)
#         mail.select(folder_name)

#         # Search for all emails
#         status, messages = mail.search(None, "ALL")

#         # Store email data
#         emails = []
#         # email_ids = messages[0].split()
#         email_ids = messages[0].split()[::-1]

#         for email_id in email_ids:
#             # Fetch the email by ID
#             res, msg = mail.fetch(email_id, "(RFC822)")
#             for response in msg:
#                 if isinstance(response, tuple):
#                     # Parse the raw email bytes
#                     msg = email.message_from_bytes(response[1])

#                     # Decode email details
#                     subject, encoding = decode_header(msg["Subject"])[0]
#                     subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject
#                     from_ = msg.get("From")
#                     date = msg.get("Date")

#                     # Extract email body (plain text or HTML)
#                     body = ""
#                     if msg.is_multipart():
#                         for part in msg.walk():
#                             content_type = part.get_content_type()
#                             if content_type == "text/plain":
#                                 body = part.get_payload(decode=True).decode(errors="ignore")
#                                 break
#                             elif content_type == "text/html":
#                                 body = part.get_payload(decode=True).decode(errors="ignore")
#                     else:
#                         body = msg.get_payload(decode=True).decode(errors="ignore")

#                     # Append email data
#                     emails.append({
#                         "id": email_id.decode(),
#                         "folder": folder_name,
#                         "from": from_,
#                         "subject": subject,
#                         "snippet": body[:100],  # Show first 100 characters
#                         "date": date
#                     })

#         # Close connection and logout
#         mail.close()
#         mail.logout()
#         return emails

#     except Exception as e:
#         print(f"Error fetching emails from {folder_name}:", e)
#         return []

# # 📌 Fetch Inbox Emails
# @app.route('/get-inbox-emails', methods=['GET'])
# def get_inbox_emails():
#     emails = fetch_emails("INBOX")
#     return jsonify(emails)

# # 📌 Fetch Spam Emails
# @app.route('/get-spam-emails', methods=['GET'])
# def get_spam_emails():
#     emails = fetch_emails("[Gmail]/Spam")  # Use "Junk" for other providers
#     return jsonify(emails)

# if __name__ == '__main__':
#     app.run(port=5001, debug=True)


# from flask import Flask, jsonify
# from flask_cors import CORS
# import imaplib
# import email
# from email.header import decode_header
# import os

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend access

# # Email credentials (Use environment variables for security)
# IMAP_SERVER = "imap.gmail.com"
# EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT", "draaft001@gmail.com")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "hxrvnhczikjuwlva")

# def fetch_emails(folder_name=None, search_criteria=None):
#     """Fetch all emails from a folder or based on search criteria, latest first."""
#     try:
#         # Connect to the IMAP server
#         mail = imaplib.IMAP4_SSL(IMAP_SERVER)
#         mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        
#         # Select the folder (Inbox, Spam, etc.) or default to Inbox for search
#         if folder_name:
#             mail.select(folder_name)
#         else:
#             mail.select("INBOX")  # Default for search-based fetches like Starred

#         # Search for emails
#         if search_criteria:
#             status, messages = mail.search(None, search_criteria)
#         else:
#             status, messages = mail.search(None, "ALL")
#         if status != "OK" or not messages[0]:
#             print(f"No emails found for {folder_name or search_criteria}")
#             mail.close()
#             mail.logout()
#             return []

#         # Get all email IDs (most recent first)
#         email_ids = messages[0].split()[::-1]  # Reverse for latest first
#         if not email_ids:
#             print("No emails to fetch")
#             mail.close()
#             mail.logout()
#             return []
        
#         emails = []

#         for email_id in email_ids:
#             # Fetch the email by ID
#             res, msg = mail.fetch(email_id, "(RFC822)")
#             for response in msg:
#                 if isinstance(response, tuple):
#                     # Parse the raw email bytes
#                     msg = email.message_from_bytes(response[1])

#                     # Decode email details
#                     subject, encoding = decode_header(msg["Subject"])[0] if msg["Subject"] else ("No Subject", None)
#                     subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject
#                     from_ = msg.get("From", "Unknown Sender")
#                     date = msg.get("Date", "Unknown Date")

#                     # Extract email body (plain text or HTML)
#                     body = ""
#                     if msg.is_multipart():
#                         for part in msg.walk():
#                             content_type = part.get_content_type()
#                             if content_type == "text/plain":
#                                 body = part.get_payload(decode=True).decode(errors="ignore")
#                                 break
#                             elif content_type == "text/html":
#                                 body = part.get_payload(decode=True).decode(errors="ignore")
#                     else:
#                         body = msg.get_payload(decode=True).decode(errors="ignore")

#                     # Append email data with both snippet and full content
#                     emails.append({
#                         "id": email_id.decode(),
#                         "folder": folder_name or "INBOX",
#                         "from": from_,
#                         "subject": subject,
#                         "snippet": body[:200],  # First 200 chars for preview (adjustable)
#                         "content": body,       # Full content for detailed view
#                         "date": date
#                     })

#         # Close connection and logout
#         mail.close()
#         mail.logout()
#         return emails

#     except Exception as e:
#         print(f"Error fetching emails from {folder_name or search_criteria}:", e)
#         return []

# # 📌 Fetch Inbox Emails
# @app.route('/get-inbox-emails', methods=['GET'])
# def get_inbox_emails():
#     emails = fetch_emails("INBOX")
#     return jsonify(emails)

# # 📌 Fetch Spam Emails
# @app.route('/get-spam-emails', methods=['GET'])
# def get_spam_emails():
#     emails = fetch_emails("[Gmail]/Spam")
#     return jsonify(emails)

# # 📌 Fetch Starred Emails
# @app.route('/get-starred-emails', methods=['GET'])
# def get_starred_emails():
#     emails = fetch_emails(search_criteria="FLAGGED")  # All starred, latest first
#     return jsonify(emails)

# # 📌 Fetch Important Emails
# @app.route('/get-important-emails', methods=['GET'])
# def get_important_emails():
#     emails = fetch_emails("[Gmail]/Important")  # All important, latest first
#     return jsonify(emails)

# if __name__ == '__main__':
#     app.run(port=5001, debug=True)



from flask import Flask, jsonify, request
from flask_cors import CORS
import imaplib
import email
from email.header import decode_header
import os
import sqlite3

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS with credential support

IMAP_SERVER = "imap.gmail.com"

def fetch_emails(email_account, email_password, folder_name=None, search_criteria=None):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        print(f"Logging in with {email_account}")
        mail.login(email_account, email_password)
        
        if folder_name:
            print(f"Selecting folder: {folder_name}")
            mail.select(folder_name)
        else:
            print("Selecting default INBOX")
            mail.select("INBOX")

        if search_criteria:
            print(f"Searching with criteria: {search_criteria}")
            status, messages = mail.search(None, search_criteria)
        else:
            print("Searching for ALL emails")
            status, messages = mail.search(None, "ALL")
        
        print(f"Search status: {status}, Message IDs: {messages[0].split()}")
        if status != "OK" or not messages[0]:
            print(f"No emails found for {folder_name or search_criteria}")
            mail.close()
            mail.logout()
            return []

        email_ids = messages[0].split()[::-1]  # Reverse for latest first
        print(f"Email IDs to fetch: {email_ids}")
        emails = []

        for email_id in email_ids:
            res, msg = mail.fetch(email_id, "(RFC822)")
            print(f"Fetch response for ID {email_id}: {res}")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0] if msg["Subject"] else ("No Subject", None)
                    subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject
                    from_ = msg.get("From", "Unknown Sender")
                    date = msg.get("Date", "Unknown Date")
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                            elif content_type == "text/html":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    emails.append({
                        "id": email_id.decode(),
                        "folder": folder_name or "INBOX",
                        "from": from_,
                        "subject": subject,
                        "snippet": body[:200],
                        "content": body,
                        "date": date
                    })

        mail.close()
        mail.logout()
        print(f"Returning {len(emails)} emails")
        return emails

    except Exception as e:
        print(f"Error fetching emails from {folder_name or search_criteria}: {e}")
        return []

# Middleware to require sender email and fetch credentials from DB
def require_sender_email(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        sender_email = request.headers.get('X-Sender-Email')  # Get email from request header
        if not sender_email:
            return jsonify({"error": "Sender email required in X-Sender-Email header"}), 400

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

            # Pass email and password to the endpoint
            kwargs['sender_email'] = sender_email
            kwargs['sender_password'] = sender_password
            return func(*args, **kwargs)

        except Exception as e:
            print(f"Error retrieving sender password: {str(e)}")
            return jsonify({"error": "Failed to retrieve sender credentials"}), 500
    return wrapper

# Fetch Inbox Emails
@app.route('/get-inbox-emails', methods=['GET'])
@require_sender_email
def get_inbox_emails(sender_email, sender_password):
    emails = fetch_emails(sender_email, sender_password, "INBOX")
    return jsonify(emails)

# Fetch Spam Emails
@app.route('/get-spam-emails', methods=['GET'])
@require_sender_email
def get_spam_emails(sender_email, sender_password):
    emails = fetch_emails(sender_email, sender_password, "[Gmail]/Spam")
    return jsonify(emails)

# Fetch Starred Emails
@app.route('/get-starred-emails', methods=['GET'])
@require_sender_email
def get_starred_emails(sender_email, sender_password):
    emails = fetch_emails(sender_email, sender_password, search_criteria="FLAGGED")
    return jsonify(emails)

# Fetch Important Emails
@app.route('/get-important-emails', methods=['GET'])
@require_sender_email
def get_important_emails(sender_email, sender_password):
    emails = fetch_emails(sender_email, sender_password, "[Gmail]/Important")
    return jsonify(emails)

# Fetch Sent Emails
@app.route('/get-sent-emails', methods=['GET'])
@require_sender_email
def get_sent_emails(sender_email, sender_password):
    emails = fetch_emails(sender_email, sender_password, "[Gmail]/Sent Mail")
    return jsonify(emails)

if __name__ == '__main__':
    app.run(port=5001, debug=True)