import os
import smtplib
from email.message import EmailMessage

SYSTEM_EMAIL = os.getenv("SYSTEM_EMAIL")
SYSTEM_PASS = os.getenv("SYSTEM_PASS")

def send_email(subject, body, to_list, cc_list):
    """
    Sends email using Gmail SMTP.
    """

    if not SYSTEM_EMAIL or not SYSTEM_PASS:
        raise RuntimeError("Email credentials not set in environment variables")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SYSTEM_EMAIL
    msg["To"] = ", ".join(to_list)
    msg["Cc"] = ", ".join(cc_list)
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SYSTEM_EMAIL, SYSTEM_PASS)
        smtp.send_message(msg)

    print(f"📧 Email Sent → {subject}")
