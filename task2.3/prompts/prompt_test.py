import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("PRIMARY_MODEL", "openai/gpt-oss-20b:free")

API_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_prompt(version):
    path = Path("prompts") / f"{version}.txt"
    return path.read_text(encoding="utf-8")


def ask_model(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    response = httpx.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


def main():
    version = "v6"

    prompt = load_prompt(version)

    print("=" * 60)
    print(f"Testing {version}")
    print("=" * 60)

    print("\nPROMPT:")
    print(prompt)

    print("\nMODEL RESPONSE:")
    result = ask_model(prompt)
    print(result)


if __name__ == "__main__":
    main()