from groq import Groq
from app.config import get_settings


def generate_summary(data_text: str) -> str:
    """Use Groq (Llama 3) to generate a professional sales narrative summary."""
    settings = get_settings()
    client = Groq(api_key=settings.groq_api_key)

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

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=4096,
    )
    return response.choices[0].message.content
