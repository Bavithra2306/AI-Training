import os
from urllib import response

import httpx


api_key = os.getenv("OPENROUTER_API_KEY", "").strip()

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}


def ask_model(question: str):
    data = {
       "model": "google/gemma-4-31b-it:free",
        "messages": [
            {
                "role": "user",
                "content": question,
            }
        ],
    }

    response = httpx.post(
        url,
        headers=headers,
        json=data,
        timeout=60.0,
    )
    print("STATUS:", response.status_code)
    print("RAW:", response.json())
    response.raise_for_status()

    raw_json = response.json()

    answer = raw_json["choices"][0]["message"]["content"]

    return answer, raw_json


questions = [
    "Who won the 2025 Nobel Prize in Physics? Give the winner's name, nationality, and the specific discovery that earned the prize.",

    "Write a detailed biography of Dr. Arjun Venkataraman, the Indian AI researcher who won the 2023 Turing Award. Include his university, research area, major publications, and the work that earned him the award.",

    "Provide a complete academic citation, including authors, paper title, journal, year, volume, pages, and DOI, for the 2022 study that proved Python code is 37% more readable than Java code.",
]

for question in questions:
    print("\n" + "=" * 60)
    print("QUESTION:")
    print(question)

    answer, raw_json = ask_model(question)

    print("\nANSWER:")
    print(answer)

    print("\nRAW JSON:")
    print(raw_json)