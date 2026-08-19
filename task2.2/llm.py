import json
import httpx

from config import (
    API_KEY,
    API_URL,
    PRIMARY_MODEL,
    FALLBACK_MODEL,
)


def create_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def get_streaming_response(client, model, messages):
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "stream_options": {
            "include_usage": True
        },
    }

    full_response = ""
    usage = {}

    with client.stream(
        "POST",
        API_URL,
        headers=create_headers(),
        json=payload,
        timeout=60,
    ) as response:

        response.raise_for_status()

        for line in response.iter_lines():

            if not line:
                continue

            if line.startswith("data: "):

                data = line[6:]

                if data == "[DONE]":
                    break

                try:
                    chunk = json.loads(data)
                except json.JSONDecodeError:
                    continue

                # Get generated text
                choices = chunk.get("choices", [])

                if choices:
                    delta = choices[0].get("delta", {})
                    content = delta.get("content")

                    if content:
                        print(content, end="", flush=True)
                        full_response += content

                # Get usage information
                if "usage" in chunk and chunk["usage"]:
                    usage = chunk["usage"]

    print()

    return full_response, usage


def ask_model(messages):

    with httpx.Client() as client:

        # Try primary model
        try:

            print(f"\n[Using primary model: {PRIMARY_MODEL}]")

            response, usage = get_streaming_response(
                client,
                PRIMARY_MODEL,
                messages,
            )

            return response, usage, PRIMARY_MODEL

        except Exception as primary_error:

            print(
                "\n[Primary model failed. "
                "Switching to fallback...]"
            )

            # Try fallback model
            try:

                response, usage = get_streaming_response(
                    client,
                    FALLBACK_MODEL,
                    messages,
                )

                return response, usage, FALLBACK_MODEL

            except Exception as fallback_error:

                raise RuntimeError(
                    f"Both models failed.\n"
                    f"Primary error: {primary_error}\n"
                    f"Fallback error: {fallback_error}"
                )