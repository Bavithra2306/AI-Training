# Task 2.1 — Model Bake-Off

## Objective

Compare different AI models for a hotel-booking assistant based on:

- Response quality
- Latency
- Cost
- Reliability
- Local vs API-based inference

The goal is to choose a model based on measured results rather than reputation.

---

## Models Tested

### OpenRouter

Four models were tested through OpenRouter:

1. `openai/gpt-oss-20b:free`
2. `nvidia/nemotron-3.5-lightning:free`
3. `dots-studio/dots-3-note-preview:free`
4. `liquid/lfm-2.5-2.6b:free`

All four models were free models, so the measured API cost was `$0`.

### Ollama

A local model was also tested using Ollama:

- `llama3.2:3b`

The model was run locally without an API charge.

---

## Test Prompts

Five prompts were created to represent realistic hotel-booking assistant tasks.

### Prompt 1 — Hotel Recommendations

Find suitable hotels in Chennai for a family staying for 3 nights. Consider location, star rating, and family-friendly facilities.

### Prompt 2 — Hotel Description

Write a short and attractive description for a 4-star hotel in Chennai with a swimming pool, free Wi-Fi, restaurant, and airport shuttle.

### Prompt 3 — Cancellation Policy

Explain a hotel cancellation policy in simple language for a customer.

### Prompt 4 — Customer Support

Write a polite response to a customer whose booking was confirmed but the hotel cannot find the reservation.

### Prompt 5 — API Debugging

Explain the most likely causes of an HTTP 422 error when creating a hotel booking and how a developer should debug it.

---

## OpenRouter Results

The OpenRouter tests successfully recorded results for the first three prompts.

| Model | Successful Prompts | Average Latency | Cost |
|---|---:|---:|---:|
| GPT-OSS 20B | 3/5 | 40.16 s | $0 |
| Nemotron 3.5 Lightning | 3/5 | 18.05 s | $0 |
| Dots 3 | 3/5 | 6.62 s | $0 |
| LFM 2.5 2.6B | 3/5 | 108.19 s | $0 |

Prompts 4 and 5 were not evaluated successfully because the OpenRouter requests returned HTTP `429 Too Many Requests`.

Therefore, these prompts are recorded as rate-limit failures rather than model-quality failures.

---

## Ollama Results

The local `llama3.2:3b` model successfully processed all five prompts.

| Prompt | Latency | Usable? |
|---|---:|---|
| 1 | 20.19 s | No |
| 2 | 28.55 s | Yes |
| 3 | 17.39 s | Yes |
| 4 | 34.68 s | Yes |
| 5 | 84.73 s | Yes |

### Ollama Summary

- Total wall-clock time: `122.65 seconds`
- Average latency: `37.11 seconds`
- Cost: `$0`
- Usable responses: `4/5`

Prompt 1 was marked unusable because the model generated specific hotel information that was not provided in the prompt, making the response unreliable for a real hotel-booking application.

Prompt 5 had the highest latency at `84.73 seconds`, although the response was technically useful.

---

## Comparison

The fastest measured OpenRouter model was:

**Dots 3 — 6.62 seconds average latency**

The local Ollama model:

**Llama 3.2 3B — 37.11 seconds average latency**

The local model had no API cost, but its inference was considerably slower than the fastest OpenRouter model.

The local model also produced usable responses for 4 out of 5 prompts.

---

## Model Failures

### GPT-OSS 20B

- Prompts 1–3: Successfully evaluated
- Prompts 4–5: HTTP 429 rate-limit errors

### Nemotron 3.5 Lightning

- Prompts 1–3: Successfully evaluated
- Prompts 4–5: HTTP 429 rate-limit errors

### Dots 3

- Prompts 1–3: Successfully evaluated
- Prompts 4–5: HTTP 429 rate-limit errors

### LFM 2.5 2.6B

- Prompts 1–3: Successfully evaluated
- Prompts 4–5: HTTP 429 rate-limit errors

### Llama 3.2 3B — Ollama

- Prompt 1: Not usable because of unreliable/invented hotel details
- Prompt 2: Usable
- Prompt 3: Usable
- Prompt 4: Usable
- Prompt 5: Usable

---

## Recommendation

Based on the measured results, I would choose **Dots 3 through OpenRouter** for this bake-off if the main priority is response speed. It had the lowest measured average latency at **6.62 seconds** and produced usable responses for all three prompts that were successfully evaluated. However, the OpenRouter tests for prompts 4 and 5 were blocked by HTTP 429 rate limits, so the comparison is incomplete for those prompts. The local **Llama 3.2 3B** model produced usable responses for **4 out of 5 prompts** with an average latency of **37.11 seconds** and no API cost. Therefore, Ollama is attractive when local execution and zero API cost are important, but the measured latency was significantly higher than the fastest OpenRouter option.

---

## Files

```text
task2.1-model-backoff/
│
├── main.py
├── ollama_bakeoff.py
├── results.json
├── ollama_results.json
└── README.md