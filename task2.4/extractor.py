import os
import httpx
import time
import httpx
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "nvidia/llama-nemotron-rerank-vl-1b-v2:free"
URL = "https://openrouter.ai/api/v1/chat/completions"


def call_model(prompt: str) -> str:

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
    }

    for attempt in range(3):

        try:
            response = httpx.post(
                URL,
                headers=headers,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            result = response.json()

            return result["choices"][0]["message"]["content"]

        except (httpx.HTTPStatusError, httpx.RequestError) as error:

            if attempt == 2:
                raise error

            wait_time = 2 ** attempt

            print(
                f"API request failed. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)