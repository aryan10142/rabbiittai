import httpx
from app.config import get_settings


def send_email(to_email: str, subject: str, html_body: str) -> dict:
    """Send an email using SendGrid HTTP API."""
    settings = get_settings()

    response = httpx.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {settings.sendgrid_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "personalizations": [{"to": [{"email": to_email}]}],
            "from": {"email": settings.sender_email, "name": "Sales Insight Automator"},
            "subject": subject,
            "content": [{"type": "text/html", "value": html_body}],
        },
        timeout=30,
    )

    if response.status_code >= 400:
        raise Exception(f"SendGrid API error {response.status_code}: {response.text}")

    return {"status": "sent", "status_code": response.status_code}
