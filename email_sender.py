import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

if not SENDGRID_API_KEY or not FROM_EMAIL:
    raise RuntimeError("SendGrid credentials not set in environment variables")


def send_email(subject, body, to_list, cc_list):
    """
    Sends email using SendGrid API (cloud-safe).
    """

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_list,
        subject=subject,
        plain_text_content=body
    )

    # Add CC recipients
    if cc_list:
        for cc in cc_list:
            message.add_cc(cc)

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        print(f"📧 Email sent → {subject}")
        print(f"SendGrid status code: {response.status_code}")

    except Exception as e:
        print("❌ SendGrid email failed")
        raise e
