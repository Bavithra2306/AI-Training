import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

MODEL_NAME = os.getenv("MODEL_NAME")


def build_prompt(question: str) -> str:
    return f"""
You are a helpful AI assistant.

Answer the following question in one short sentence.

Question:
{question}
"""


def call_model(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content


def main():
    question = "What is Redis?"

    prompt = build_prompt(question)

    raw_response = call_model(prompt)

    final_output = raw_response.strip()

    print(final_output)


if __name__ == "__main__":
    main()