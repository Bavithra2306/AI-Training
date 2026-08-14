import os
import httpx

api_key = os.getenv("OPENROUTER_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
}

response = httpx.get(
    "https://openrouter.ai/api/v1/models",
    headers=headers,
)

print("Status:", response.status_code)
print(response.json())