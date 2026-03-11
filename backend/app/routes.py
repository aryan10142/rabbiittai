from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import EmailStr
import re
import logging

from app.file_parser import parse_file, dataframe_to_summary_text
from app.ai_engine import generate_summary
from app.email_service import send_email
from app.config import get_settings

logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


@router.post(
    "/analyze",
    summary="Upload sales data and send AI summary via email",
    response_description="Confirmation that the summary was generated and emailed",
    responses={
        200: {
            "description": "Summary generated and email sent successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Summary generated and sent to user@example.com",
                        "summary_preview": "<h2>Executive Summary...</h2>",
                    }
                }
            },
        },
        400: {"description": "Invalid file or email"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
    },
)
@limiter.limit("10/minute")
async def analyze_and_send(
    request: Request,
    file: UploadFile = File(..., description="A .csv or .xlsx sales data file"),
    email: str = Form(..., description="Recipient email address"),
):
    """
    Upload a `.csv` or `.xlsx` sales data file along with a recipient email.

    The server will:
    1. Parse and validate the uploaded file.
    2. Send the data to an AI engine (Google Gemini) to generate a professional executive summary.
    3. Email the summary to the provided address.
    """
    # Validate email format
    if not EMAIL_REGEX.match(email):
        raise HTTPException(status_code=400, detail="Invalid email address format.")

    settings = get_settings()

    # Check file size
    contents = await file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {settings.max_upload_size_mb} MB.",
        )
    await file.seek(0)

    # Parse file
    df = await parse_file(file)

    # Generate AI summary
    data_text = dataframe_to_summary_text(df)
    try:
        summary_html = generate_summary(data_text)
        logger.info("AI summary generated successfully")
    except Exception as exc:
        logger.error(f"AI summary generation failed: {exc}")
        raise HTTPException(
            status_code=500, detail=f"AI summary generation failed: {exc}"
        )

    # Send email
    try:
        send_email(
            to_email=email,
            subject="Sales Insight Report — AI-Generated Summary",
            html_body=summary_html,
        )
        logger.info(f"Email sent to {email}")
    except Exception as exc:
        logger.error(f"Email delivery failed: {exc}")
        raise HTTPException(status_code=500, detail=f"Email delivery failed: {exc}")

    return {
        "status": "success",
        "message": f"Summary generated and sent to {email}",
        "summary_preview": summary_html[:500] + "..." if len(summary_html) > 500 else summary_html,
    }


@router.get(
    "/health",
    summary="Health check",
    response_description="Service health status",
)
async def health_check():
    """Returns the health status of the API."""
    return {"status": "healthy"}
