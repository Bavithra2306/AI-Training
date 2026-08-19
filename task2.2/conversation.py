SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a helpful and concise assistant."
}


def create_conversation():
    return [SYSTEM_MESSAGE.copy()]


def add_user_message(messages, content):
    messages.append({
        "role": "user",
        "content": content
    })


def add_assistant_message(messages, content):
    messages.append({
        "role": "assistant",
        "content": content
    })