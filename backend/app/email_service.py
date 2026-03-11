import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import get_settings


def send_email(to_email: str, subject: str, html_body: str) -> dict:
    """Send an email using Gmail SMTP."""
    settings = get_settings()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Sales Insight Automator <{settings.smtp_email}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
        server.login(settings.smtp_email, settings.smtp_password)
        server.sendmail(settings.smtp_email, to_email, msg.as_string())

    return {"status": "sent"}
