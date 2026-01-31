import smtplib
from core.config import settings
from email.mime.text import MIMEText

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_SENDER
    msg["To"] = to_email

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(settings.EMAIL_SENDER, settings.EMAIL_SENDER_PASS)
        server.send_message(msg)


import requests

def send_email_sendgrid(to_email: str, subject: str, body: str):
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {settings.SENDGRID_API}",
        "Content-Type": "application/json"
    }
    data = {
        "personalizations": [{
            "to": [{"email": to_email}],
            "subject": subject
        }],
        "from": {"email": "noreply@example.com"},
        "content": [{
            "type": "text/plain",
            "value": body
        }]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code


def send_activation_email(user_email: str, token: str):
    subject = "Account Activation"
    body = f"Please click the following link to activate your account: https://yourapp.com/activate?token={token}"
    send_email(user_email, subject, body)

email = "artur.bashyrov@gmail.com"

send_activation_email(user_email=email, token="4234234")