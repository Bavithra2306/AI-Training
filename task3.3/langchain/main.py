import os

from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()


prompt = ChatPromptTemplate.from_template(
    """
You are a helpful AI assistant.

Answer the following question in one short sentence.

Question:
{question}
"""
)


model = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)


parser = StrOutputParser()


chain = prompt | model | parser


def main():
    question = "What is Redis?"

    result = chain.invoke(
        {
            "question": question
        }
    )

    print(result)


if __name__ == "__main__":
    main()