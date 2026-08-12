# ...existing code...
import os
import sys
import httpx

api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
if not api_key:
    sys.stderr.write("ERROR: OPENROUTER_API_KEY not set\n")
    raise SystemExit(1)

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

    try:
        response = httpx.post(
            url,
            headers=headers,
            json=data,
            timeout=60.0,
        )
    except httpx.HTTPError as e:
        sys.stderr.write(f"HTTPX ERROR: {e}\n")
        raise

    sys.stdout.write(f"STATUS: {response.status_code}\n")

    try:
        raw_json = response.json()
    except ValueError:
        raw_json = {"error": "invalid json", "text": response.text}

    if response.status_code >= 400:
        sys.stderr.write(f"API ERROR: {raw_json}\n")
        response.raise_for_status()

    choices = raw_json.get("choices")
    if not choices or not isinstance(choices, list):
        sys.stderr.write(f"Unexpected response structure: {raw_json}\n")
        raise SystemExit(1)

    answer = choices[0].get("message", {}).get("content", "")
    return answer, raw_json
# ...existing code...
questions = [
    "Who won the 2025 Nobel Prize in Physics? Give the winner's name, nationality, and the specific discovery that earned the prize.",

    "Write a detailed biography of Dr. Arjun Venkataraman, the Indian AI researcher who won the 2023 Turing Award. Include his university, research area, major publications, and the work that earned him the award.",

    "Provide a complete academic citation, including authors, paper title, journal, year, volume, pages, and DOI, for the 2022 study that proved Python code is 37% more readable than Java code.",
]
# ...existing code...
for question in questions:
    print("\n" + "=" * 60)

    print("QUESTION:")
    print(question)

    answer, raw_json = ask_model(question)

    print("\nANSWER:")
    print(answer)

    print("\nRAW JSON:")
    print(raw_json)
# ...existing code...