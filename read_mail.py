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

from flask import Flask, jsonify
from flask_cors import CORS
import imaplib
import email
from email.header import decode_header
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Email credentials (Use environment variables for security)
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT", "draaft001@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "hxrvnhczikjuwlva")

def fetch_emails(folder_name):
    """Fetch emails from a specific folder (Inbox or Spam)."""
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        
        # Select the folder (Inbox, Spam, or Junk)
        mail.select(folder_name)

        # Search for all emails
        status, messages = mail.search(None, "ALL")

        # Store email data
        emails = []
        email_ids = messages[0].split()

        for email_id in email_ids:
            # Fetch the email by ID
            res, msg = mail.fetch(email_id, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # Parse the raw email bytes
                    msg = email.message_from_bytes(response[1])

                    # Decode email details
                    subject, encoding = decode_header(msg["Subject"])[0]
                    subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject
                    from_ = msg.get("From")
                    date = msg.get("Date")

                    # Extract email body (plain text or HTML)
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

                    # Append email data
                    emails.append({
                        "id": email_id.decode(),
                        "folder": folder_name,
                        "from": from_,
                        "subject": subject,
                        "snippet": body[:100],  # Show first 100 characters
                        "date": date
                    })

        # Close connection and logout
        mail.close()
        mail.logout()
        return emails

    except Exception as e:
        print(f"Error fetching emails from {folder_name}:", e)
        return []

# 📌 Fetch Inbox Emails
@app.route('/get-inbox-emails', methods=['GET'])
def get_inbox_emails():
    emails = fetch_emails("INBOX")
    return jsonify(emails)

# 📌 Fetch Spam Emails
@app.route('/get-spam-emails', methods=['GET'])
def get_spam_emails():
    emails = fetch_emails("[Gmail]/Spam")  # Use "Junk" for other providers
    return jsonify(emails)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
