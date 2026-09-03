import json
import os

from openai import OpenAI
from dotenv import load_dotenv
from schemas import tools
from tools import fetch_user, calculate


load_dotenv()

MAX_ITERATIONS = 5

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def execute_tool(tool_name, arguments):
    if tool_name == "fetch_user":
        return fetch_user(**arguments)

    if tool_name == "calculate":
        return calculate(**arguments)

    return {
        "error": f"Unknown tool: {tool_name}"
    }


def run_tool_loop(user_message):
    messages = [
        {
            "role": "user",
            "content": user_message
        }
    ]

    for iteration in range(MAX_ITERATIONS):

        print(f"\n--- Iteration {iteration + 1} ---")

        response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message
        
        # No tool call means the model is finished
        if not message.tool_calls:
            return message.content

        # Add the model's tool-call message
        messages.append(message)

        # Execute every requested tool
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print(
                f"Tool requested: {tool_name}"
            )

            print(
                f"Arguments: {arguments}"
            )

            result = execute_tool(
                tool_name,
                arguments
            )

            print(
                f"Tool result: {result}"
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                }
            )

    return "Maximum iteration limit reached."