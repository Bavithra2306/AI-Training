import os
import time
import logging

import httpx
import tiktoken
from dotenv import load_dotenv


# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY", "").strip()

if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY is not set")


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

url = "https://openrouter.ai/api/v1/chat/completions"

model = "nvidia/nemotron-3.5-lightning:free"

messages = [
    {
        "role": "user",
        "content": "Tell me what Python is.",
    },
]


# ------------------------------------------------------------
# Token counting
# ------------------------------------------------------------

encoding = tiktoken.get_encoding("cl100k_base")

prompt_text = messages[0]["content"]

prompt_tokens_before = len(
    encoding.encode(prompt_text)
)

print(f"Prompt tokens before request: {prompt_tokens_before}")


# ------------------------------------------------------------
# Request
# ------------------------------------------------------------

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

data = {
    "model": model,
    "messages": messages,
}


# ------------------------------------------------------------
# Start timer
# ------------------------------------------------------------

start_time = time.perf_counter()

response = httpx.post(
    url,
    headers=headers,
    json=data,
    timeout=30.0,
)

end_time = time.perf_counter()


# ------------------------------------------------------------
# Calculate latency
# ------------------------------------------------------------

latency_ms = (end_time - start_time) * 1000


# ------------------------------------------------------------
# Check response
# ------------------------------------------------------------

response.raise_for_status()

result = response.json()


# ------------------------------------------------------------
# Read provider usage
# ------------------------------------------------------------

usage = result.get("usage", {})

prompt_tokens = usage.get("prompt_tokens", 0)
completion_tokens = usage.get("completion_tokens", 0)

total_tokens = usage.get(
    "total_tokens",
    prompt_tokens + completion_tokens,
)


# ------------------------------------------------------------
# Cost calculation
# ------------------------------------------------------------

input_price_per_million = 0.0
output_price_per_million = 0.0

input_cost = (
    prompt_tokens / 1_000_000
) * input_price_per_million

output_cost = (
    completion_tokens / 1_000_000
) * output_price_per_million

cost_usd = input_cost + output_cost


# ------------------------------------------------------------
# USD -> INR
# ------------------------------------------------------------

usd_to_inr = 88.0

cost_inr = cost_usd * usd_to_inr


# ------------------------------------------------------------
# Print results
# ------------------------------------------------------------

print()
print("========== TOKEN AND COST REPORT ==========")

print(f"Model: {model}")

print(
    f"Prompt tokens before request: "
    f"{prompt_tokens_before}"
)

print(
    f"Provider prompt tokens: "
    f"{prompt_tokens}"
)

print(
    f"Completion tokens: "
    f"{completion_tokens}"
)

print(
    f"Total tokens: "
    f"{total_tokens}"
)

print(
    f"Latency: "
    f"{latency_ms:.2f} ms"
)

print(
    f"Cost USD: "
    f"${cost_usd:.8f}"
)

print(
    f"Cost INR: "
    f"₹{cost_inr:.6f}"
)


# ------------------------------------------------------------
# Structured logging
# ------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

logging.info(
    "token_cost_report "
    f"model={model} "
    f"prompt_tokens_before={prompt_tokens_before} "
    f"prompt_tokens={prompt_tokens} "
    f"completion_tokens={completion_tokens} "
    f"total_tokens={total_tokens} "
    f"latency_ms={latency_ms:.2f} "
    f"cost_usd={cost_usd:.8f} "
    f"cost_inr={cost_inr:.6f}"
)


# ------------------------------------------------------------
# Print assistant response
# ------------------------------------------------------------

print()
print("========== ASSISTANT RESPONSE ==========")

print(
    result["choices"][0]["message"]["content"]
)