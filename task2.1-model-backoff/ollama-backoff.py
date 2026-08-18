import asyncio
import json
import time

import httpx


OLLAMA_URL = "http://localhost:11434/api/chat"

MODEL = "llama3.2:3b"


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


async def ask_ollama(client, prompt_number, prompt):

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "stream": False,
    }

    start_time = time.perf_counter()

    try:

        response = await client.post(
            OLLAMA_URL,
            json=data,
        )

        latency = time.perf_counter() - start_time

        response.raise_for_status()

        result = response.json()

        answer = result["message"]["content"]

        prompt_tokens = result.get(
            "prompt_eval_count",
            0,
        )

        completion_tokens = result.get(
            "eval_count",
            0,
        )

        total_tokens = (
            prompt_tokens + completion_tokens
        )

        return {
            "prompt_number": prompt_number,
            "model": MODEL,
            "answer": answer,
            "latency": latency,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost": 0.0,
            "error": None,
        }

    except httpx.HTTPError as error:

        latency = time.perf_counter() - start_time

        return {
            "prompt_number": prompt_number,
            "model": MODEL,
            "answer": None,
            "latency": latency,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "cost": 0.0,
            "error": str(error),
        }


async def main():

    # Maximum 2 Ollama requests at the same time
    semaphore = asyncio.Semaphore(2)

    async def limited_request(
        client,
        prompt_number,
        prompt,
    ):

        async with semaphore:

            return await ask_ollama(
                client,
                prompt_number,
                prompt,
            )

    start_time = time.perf_counter()

    async with httpx.AsyncClient(
        timeout=300
    ) as client:

        tasks = [
            asyncio.create_task(
                limited_request(
                    client,
                    prompt_number,
                    prompt,
                )
            )
            for prompt_number, prompt in enumerate(
                PROMPTS,
                start=1,
            )
        ]

        results = []

        # Process each result as soon as it finishes
        for completed_task in asyncio.as_completed(tasks):

            result = await completed_task

            results.append(result)

            print("\n" + "#" * 70)

            print(
                "PROMPT:",
                result["prompt_number"],
            )

            print("#" * 70)

            print("\nMODEL:")
            print(result["model"])

            print("\nLATENCY:")
            print(
                round(result["latency"], 2),
                "seconds",
            )

            if result["error"]:

                print("\nERROR:")
                print(result["error"])

            else:

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
                    result["cost"],
                )

    total_time = time.perf_counter() - start_time

    # Sort results by prompt number
    results.sort(
        key=lambda result: result["prompt_number"]
    )

    with open(
        "ollama_results.json",
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("\n" + "=" * 70)

    print("TOTAL WALL-CLOCK TIME:")

    print(
        round(total_time, 2),
        "seconds",
    )

    print(
        "\nResults saved to ollama_results.json"
    )


if __name__ == "__main__":
    asyncio.run(main())