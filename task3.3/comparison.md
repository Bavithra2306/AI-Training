# Manual vs LangChain

## 1. Prompt construction

### Manual

I created a Python function:

`build_prompt()`

and manually inserted the user's question into the prompt.

### LangChain

LangChain provides:

`ChatPromptTemplate`

It handles the prompt template and variable insertion.

### Verdict

Worth handing over: YES

Prompt templating is repetitive infrastructure. LangChain makes it easier to compose prompts with other components.

---

## 2. Model invocation

### Manual

I directly called:

`client.chat.completions.create()`

and manually created the messages structure.

### LangChain

`ChatOpenAI` handles the model interaction and converts the model into a chain-compatible component.

### Verdict

Worth handing over: YES

This removes provider-specific API plumbing and makes the model easier to connect to other LangChain components.

---

## 3. Response extraction

### Manual

I manually accessed:

`response.choices[0].message.content`

### LangChain

The model returns a LangChain message object that can be passed directly to the next component.

### Verdict

Worth handing over: YES

This removes repetitive response-object navigation.

---

## 4. Output parsing

### Manual

I manually converted/cleaned the response using:

`raw_response.strip()`

### LangChain

`StrOutputParser` handles converting the model message into a string.

### Verdict

Worth handing over: YES

This becomes especially useful when more structured output parsing is required.

---

## 5. Pipeline composition

### Manual

I explicitly called each function:

build_prompt()
→ call_model()
→ output processing

### LangChain

LCEL allows the pipeline to be expressed as:

prompt | model | parser

### Verdict

Worth handing over: YES

The pipeline becomes easier to read and extend.

# Callback Hook

LangChain supports callbacks around chain/model execution.

The callback hook can be used to observe what happens during the chain execution.

For example, in Week 6 we can attach tracing/observability to this hook to capture:

- chain start
- model start
- model response
- token usage
- execution time
- errors

This will allow us to monitor the AI pipeline without adding logging code throughout the application.