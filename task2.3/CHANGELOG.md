# Prompt Iteration Log

## Task

Extract structured information from a customer complaint.

The prompt should extract:
- Customer name
- Order ID
- Date
- Problem
- Requested solution

---

## Version 1 — Baseline

### What changed

This was the original baseline prompt. No previous version existed.

### What I expected

I expected the model to identify the customer information, order ID, date, problem, and requested solution from the complaint.

### What actually happened

The model correctly extracted all five pieces of information, but returned them as a Markdown table.

### Result

The information was correct, but the output was not in a structured format such as JSON, which would be more useful for programmatic processing.

---

## Version 2

### What changed

Added one instruction:

> Return the extracted information as JSON.

No other part of the prompt was changed.

### What I expected

I expected the model to return the same five pieces of information in JSON format.

### What actually happened

The model returned valid JSON containing all five requested fields:

- customer
- order_id
- date
- problem
- requested_solution

### Result

The output format improved from a Markdown table to JSON while preserving the extracted information.

## Version 3 — Few-shot Example

### What changed

Added one example showing a customer complaint and its expected JSON output.

### What I expected

I expected the example to help the model understand the required JSON structure and produce consistent field names.

### What actually happened

The model returned valid JSON using the same five-field structure as the example.

### Result

The prompt continued to extract the correct information, and the output followed the demonstrated structure.

---

## Version 4 — Negative Instruction

### What changed

Added one instruction:

> Do not include any explanation or extra text.

### What I expected

I expected the model to return only the JSON object without additional explanation or formatting.

### What actually happened

The model returned only the JSON object, without additional explanation.

### Result

The output became cleaner and remained correct.

---

## Version 5 — Delimiters

### What changed

Wrapped the customer complaint in `<complaint>` and `</complaint>` tags.

### What I expected

I expected the delimiters to clearly separate the complaint data from the instructions and example.

### What actually happened

The model returned valid JSON containing all five requested fields. The problem description was also captured more completely than in Version 4.

### Result

The delimiter change preserved the correct output and slightly improved the completeness of the extracted problem description.

---

## Version 6 — Conflicting Negative Instruction

### What changed

Added one instruction:

> Do not include the requested solution in the output.

### What I expected

I expected this conflicting negative instruction to cause the model to omit the requested solution, making the output incomplete.

### What actually happened

The model omitted the `requested_solution` field from the JSON response.

### Result

This version made the prompt worse because the original task explicitly required extracting the requested solution, but the new instruction caused that required field to be removed.