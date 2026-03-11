import httpx
from app.config import get_settings


def send_email(to_email: str, subject: str, html_body: str) -> dict:
    """Send an email using Mailjet HTTP API."""
    settings = get_settings()

    response = httpx.post(
        "https://api.mailjet.com/v3.1/send",
        auth=(settings.mailjet_api_key, settings.mailjet_secret_key),
        json={
            "Messages": [
                {
                    "From": {
                        "Email": settings.sender_email,
                        "Name": "Sales Insight Automator",
                    },
                    "To": [{"Email": to_email}],
                    "Subject": subject,
                    "HTMLPart": html_body,
                }
            ]
        },
        timeout=30,
    )

    if response.status_code >= 400:
        raise Exception(f"Mailjet API error {response.status_code}: {response.text}")

    return response.json()
