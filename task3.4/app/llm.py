from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    return ChatOpenAI(
        model="nvidia/nemotron-3.5-lightning:free",
        api_key= os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        temperature=0
    )


def call_llm(question: str) -> str:
    llm = get_llm()

    prompt = PROMPT.format(question=question)

    response = llm.invoke(prompt)

    return response.content


PROMPT = """You are a helpful technical assistant.

Answer the user's question accurately and concisely.
If the question is unsafe or requests harmful instructions,
refuse to provide those instructions.

Question: {question}
"""