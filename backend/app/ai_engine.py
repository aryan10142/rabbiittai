import google.generativeai as genai
from app.config import get_settings


def generate_summary(data_text: str) -> str:
    """Use Google Gemini to generate a professional sales narrative summary."""
    settings = get_settings()
    genai.configure(api_key=settings.gemini_api_key)

    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""You are a senior business analyst. Analyze the following sales data and 
produce a professional executive summary suitable for C-level leadership.

The summary should include:
1. **Overview** – high-level performance snapshot.
2. **Key Metrics** – total revenue, units sold, average order value, etc.
3. **Regional Performance** – breakdown by region.
4. **Product Category Insights** – performance per category.
5. **Trends & Observations** – notable patterns or concerns.
6. **Recommendations** – 2-3 actionable next steps.

Format the output in clean HTML suitable for an email body (use <h2>, <p>, <ul>, <table> tags).
Do NOT include ```html fences. Return raw HTML only.

--- DATA START ---
{data_text}
--- DATA END ---
"""

    response = model.generate_content(prompt)
    return response.text
