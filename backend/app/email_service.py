import httpx
from app.config import get_settings


def send_email(to_email: str, subject: str, html_body: str) -> dict:
    """Send an email using Brevo (Sendinblue) transactional email HTTP API."""
    settings = get_settings()

    response = httpx.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "api-key": settings.brevo_api_key,
            "Content-Type": "application/json",
            "accept": "application/json",
        },
        json={
            "sender": {"name": "Sales Insight", "email": settings.sender_email},
            "to": [{"email": to_email}],
            "subject": subject,
            "htmlContent": html_body,
        },
        timeout=30,
    )

    if response.status_code >= 400:
        raise Exception(f"Brevo API error {response.status_code}: {response.text}")

    return response.json()
