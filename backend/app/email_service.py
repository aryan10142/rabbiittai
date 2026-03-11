import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import get_settings


def send_email(to_email: str, subject: str, html_body: str) -> dict:
    """Send an email with the generated summary using Gmail SMTP."""
    settings = get_settings()

    msg = MIMEMultipart("alternative")
    msg["From"] = settings.smtp_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as server:
        server.starttls()
        server.login(settings.smtp_email, settings.smtp_password)
        server.sendmail(settings.smtp_email, to_email, msg.as_string())

    return {"status": "sent", "to": to_email}
