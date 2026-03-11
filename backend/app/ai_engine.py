from groq import Groq
from app.config import get_settings


def generate_summary(data_text: str) -> str:
    """Use Groq (Llama 3) to generate a professional sales narrative summary."""
    settings = get_settings()
    client = Groq(api_key=settings.groq_api_key)

    prompt = f"""Analyze this sales data and produce a concise executive summary in HTML.
Include: Overview, Key Metrics (revenue, units, avg order), Regional Performance, Category Insights, Trends, and 2-3 Recommendations.
Use <h2>, <p>, <ul>, <table> tags. Return raw HTML only, no markdown fences.

{data_text}"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=3000,
    )
    return response.choices[0].message.content
