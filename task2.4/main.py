import json
import re

from pydantic import ValidationError

from models import CustomerComplaint
from extractor import call_model


def clean_json_response(content: str) -> str:
    content = content.strip()

    if content.startswith("```json"):
        content = content[7:]

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()

    start = content.find("{")
    end = content.rfind("}")

    if start != -1 and end != -1:
        content = content[start:end + 1]

    content = re.sub(r",\s*([}\]])", r"\1", content)

    return content


def extract(text: str):
    prompt = f"""
Extract the customer complaint information from the text below.

Return ONLY valid JSON.

Required fields:
- customer
- order_id
- date
- problem
- requested_solution

Text:
{text}
"""

    # First attempt
    raw_content = call_model(prompt)

    try:
        cleaned_content = clean_json_response(raw_content)
        data = json.loads(cleaned_content)

        complaint = CustomerComplaint.model_validate(data)

        return complaint, "success"

    except (json.JSONDecodeError, ValidationError) as error:

        # Retry once
        retry_prompt = f"""
Your previous response could not be accepted.

The error was:

{error}

Please correct the response and return ONLY valid JSON.

Required fields:
- customer
- order_id
- date
- problem
- requested_solution

Original text:
{text}
"""

        raw_content = call_model(retry_prompt)

        try:
            cleaned_content = clean_json_response(raw_content)
            data = json.loads(cleaned_content)

            complaint = CustomerComplaint.model_validate(data)

            return complaint, "recovered"

        except (json.JSONDecodeError, ValidationError) as retry_error:

            return retry_error, "failed"