

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def call_llm(temperature, prompt):
    payload = {
        "model": "nvidia/nemotron-3.5-lightning:free",
        "messages": [
            {
                "role": "user",
                "content": prompt 
            }
        ],
        "temperature": temperature,
    }

    response = httpx.post(
        URL,
        headers=headers,
        json=payload,
        timeout=30.0,
    )
    print("Status:", response.status_code)
    print("Response:", response.text)

    
    data = response.json()

    usage = data.get("usage", {})

    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)

    print("Prompt tokens:", prompt_tokens)
    print("Completion tokens:", completion_tokens)
    print("Total tokens:", total_tokens)

    
    return data["choices"][0]["message"]["content"]





large_prompt = "Explain APIs in detail. " * 55000

answer = call_llm(0, large_prompt)

print("Answer:", answer)
