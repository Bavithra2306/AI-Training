import os, time
import asyncio
import httpx
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# Get API key
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not set")


# OpenRouter API details
API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL = "nvidia/nemotron-nano-9b-v2:free"

# Read prompts from prompts.txt
def load_prompts(filename):
    with open(filename, "r", encoding="utf-8") as file:
        prompts = [
            line.strip()
            for line in file
            if line.strip()
        ]

    return prompts


# Send one prompt to the model
async def ask_model(client, prompt):

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

    for attempt in range(3):

        response = await client.post(
            API_URL,
            headers=headers,
            json=payload,
        )

        if response.status_code == 429:
            wait_time = 2 ** attempt

            print(
                f"Rate limited. Waiting {wait_time} seconds..."
            )

            await asyncio.sleep(wait_time)
            continue

        response.raise_for_status()

        return response.json()


    raise RuntimeError("Request failed after 3 attempts")


#sequential execution for comparison
async def run_sequential(prompts, client):

    start_time = time.perf_counter()

    results = []

    for prompt in prompts:
        result = await ask_model(client, prompt)
        results.append(result)

    elapsed_time = time.perf_counter() - start_time

    return results, elapsed_time

# concurrent execution for comparison
async def run_concurrent(prompts, client):

    start_time = time.perf_counter()

    tasks = [
        ask_model(client, prompt)
        for prompt in prompts
    ]

    results = await asyncio.gather(*tasks)

    elapsed_time = time.perf_counter() - start_time

    return results, elapsed_time

# Token usage and cost calculation

INPUT_PRICE_PER_MILLION = 0.0
OUTPUT_PRICE_PER_MILLION = 0.0

def calculate_cost(usage):
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)

    input_cost = (
        prompt_tokens / 1_000_000
    ) * INPUT_PRICE_PER_MILLION

    output_cost = (
        completion_tokens / 1_000_000
    ) * OUTPUT_PRICE_PER_MILLION

    return input_cost + output_cost

# Main function with concurrency
async def main():

    prompts = load_prompts("task5/prompts.txt")

    print(f"Loaded {len(prompts)} prompts")

    async with httpx.AsyncClient(timeout=30) as client:

        print("\nRunning sequential batch...")

        sequential_results, sequential_time = await run_sequential(
            prompts,
            client
        )

        print("\nRunning concurrent batch...")

        concurrent_results, concurrent_time = await run_concurrent(
            prompts,
            client
        )

    # Use concurrent results for batch cost
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_tokens = 0
    total_cost = 0.0

    for result in concurrent_results:

        usage = result.get("usage", {})

        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)

        tokens = usage.get(
            "total_tokens",
            prompt_tokens + completion_tokens
        )

        total_prompt_tokens += prompt_tokens
        total_completion_tokens += completion_tokens
        total_tokens += tokens

        total_cost += calculate_cost(usage)

    average_cost = total_cost / len(concurrent_results)

    speedup = sequential_time / concurrent_time

    print("\n========== BATCH REPORT ==========")

    print(f"Prompts processed: {len(prompts)}")

    print(f"\nSequential time: {sequential_time:.2f} seconds")
    print(f"Concurrent time: {concurrent_time:.2f} seconds")
    print(f"Speedup: {speedup:.2f}x")

    print(f"\nPrompt tokens: {total_prompt_tokens}")
    print(f"Completion tokens: {total_completion_tokens}")
    print(f"Total tokens: {total_tokens}")

    print(f"\nTotal cost: ${total_cost:.6f}")
    print(f"Average cost per prompt: ${average_cost:.6f}")

    print("==================================")

# Program starts here
if __name__ == "__main__":
    asyncio.run(main())