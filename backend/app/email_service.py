import resend
from app.config import get_settings


def send_email(to_email: str, subject: str, html_body: str) -> dict:
    """Send an email with the generated summary using Resend."""
    settings = get_settings()
    resend.api_key = settings.resend_api_key

    params: resend.Emails.SendParams = {
        "from": settings.from_email,
        "to": [to_email],
        "subject": subject,
        "html": html_body,
    }

    response = resend.Emails.send(params)
    return response
