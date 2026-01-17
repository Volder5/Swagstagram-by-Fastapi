import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
load_dotenv()

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")



def send_email(to_email: str, subject: str, content: str):
    sender_email = EMAIL_HOST_USER
    sender_password = EMAIL_HOST_PASSWORD

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)