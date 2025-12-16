import smtplib
from email.message import EmailMessage

SYSTEM_EMAIL = "bbn.nitt@gmail.com"
SYSTEM_PASS = "tlar dgao kirq ztos"  


def send_email(subject, body, to_list, cc_list):
    """
    Sends email using Gmail SMTP.
    """
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
