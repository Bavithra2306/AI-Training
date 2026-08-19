import os
import json
import time
import asyncio
import httpx

from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"


PROMPTS = [
    "Find suitable hotels in Chennai for a family staying for 3 nights. "
    "Consider location, star rating, and family-friendly facilities.",

    "Write a short and attractive description for a 4-star hotel "
    "in Chennai with a swimming pool, free Wi-Fi, restaurant, and airport shuttle.",

    "Explain this hotel cancellation policy in simple language for a customer: "
    "Free cancellation is available up to 48 hours before check-in. "
    "Cancellations within 48 hours will be charged one night's stay.",

    "A customer says their booking was confirmed but the hotel cannot find "
    "the reservation. Write a polite customer-support response with the "
    "next steps the customer should take.",

    "A hotel booking API returns HTTP 422 when a customer tries to create "
    "a booking. Explain the most likely causes and how a developer should "
    "debug the problem.",
]


MODELS = [
    "openai/gpt-oss-20b:free",
    "nvidia/nemotron-3.5-lightning:free",
    "dots-studio/dots-3-note-preview:free",
    "liquid/lfm-2.5-2.6b:free",
]


PRICING = {
    "openai/gpt-oss-20b:free": {
        "input": 0.0,
        "output": 0.0,
    },

    "nvidia/nemotron-3.5-lightning:free": {
        "input": 0.0,
        "output": 0.0,
    },

    "dots-studio/dots-3-note-preview:free": {
        "input": 0.0,
        "output": 0.0,
    },

    "liquid/lfm-2.5-2.6b:free": {
        "input": 0.0,
        "output": 0.0,
    },
}


# Maximum 3 requests can run at the same time
semaphore = asyncio.Semaphore(3)


async def ask_model(client, prompt_number, prompt, model):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    async with semaphore:

        start_time = time.perf_counter()

        try:

            response = await client.post(
                URL,
                headers=headers,
                json=data,
            )

            latency = time.perf_counter() - start_time

            response.raise_for_status()

        except httpx.HTTPStatusError as error:

            print(
                f"\nERROR - {model} - Prompt {prompt_number}: "
                f"HTTP {error.response.status_code}"
            )

            return None

        except httpx.ConnectError:

            print(
                f"\nERROR - {model} - Prompt {prompt_number}: "
                f"Connection failed"
            )

            return None

        except httpx.TimeoutException:

            print(
                f"\nERROR - {model} - Prompt {prompt_number}: "
                f"Request timed out"
            )

            return None

    result = response.json()

    answer = result["choices"][0]["message"]["content"]

    usage = result.get("usage", {})

    prompt_tokens = usage.get(
        "prompt_tokens",
        0,
    )

    completion_tokens = usage.get(
        "completion_tokens",
        0,
    )

    total_tokens = usage.get(
        "total_tokens",
        prompt_tokens + completion_tokens,
    )

    pricing = PRICING[model]

    input_cost = (
        prompt_tokens / 1_000_000
    ) * pricing["input"]

    output_cost = (
        completion_tokens / 1_000_000
    ) * pricing["output"]

    total_cost = input_cost + output_cost

    return {
        "prompt_number": prompt_number,
        "model": model,
        "answer": answer,
        "latency": latency,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "cost": total_cost,
    }


async def main():

    all_results = []

    async with httpx.AsyncClient(timeout=60) as client:

        tasks = []

        for prompt_number, prompt in enumerate(
            PROMPTS,
            start=1,
        ):

            for model in MODELS:

                task = asyncio.create_task(
                    ask_model(
                        client,
                        prompt_number,
                        prompt,
                        model,
                    )
                )

                tasks.append(task)

        # Process each task whenever it finishes
        for completed_task in asyncio.as_completed(tasks):

            result = await completed_task

            if result is None:
                continue

            all_results.append(result)

            print("\n" + "=" * 70)

            print(
                f"PROMPT: {result['prompt_number']}"
            )

            print(
                f"MODEL: {result['model']}"
            )

            print(
                f"LATENCY: "
                f"{round(result['latency'], 2)} seconds"
            )

            print("\nANSWER:")
            print(result["answer"])

            print("\nTOKENS:")

            print(
                "Prompt:",
                result["prompt_tokens"],
            )

            print(
                "Completion:",
                result["completion_tokens"],
            )

            print(
                "Total:",
                result["total_tokens"],
            )

            print("\nCOST:")

            print(
                "$",
                round(result["cost"], 8),
            )

            # Save immediately after every successful call
            with open(
                "results.json",
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    all_results,
                    file,
                    indent=2,
                    ensure_ascii=False,
                )

    print(
        "\nResults saved to results.json"
    )


if __name__ == "__main__":
    asyncio.run(main())