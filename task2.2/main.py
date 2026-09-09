from llm import ask_model
from conversation import (
    create_conversation,
    add_user_message,
    add_assistant_message,
)
from cost import calculate_cost, get_token_counts,  get_cache_counts


def main():

    messages = create_conversation()

    total_cost = 0.0
    turn_number = 0

    print("=" * 60)
    print("Task 2.2 - Real Conversation")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("\nGoodbye! 👋")
            break

        if not user_input:
            continue

        turn_number += 1

        # Add the new user message to history
        add_user_message(messages, user_input)

        try:

            # Send the entire conversation history
            response, usage, model_used = ask_model(messages)

            # Add assistant response to history
            add_assistant_message(messages, response)

            # Get token usage
            prompt_tokens, completion_tokens, total_tokens = (
                get_token_counts(usage)
            )
            cached_tokens, cache_write_tokens = (
                get_cache_counts(usage)
            )

            # Calculate this turn's cost
            turn_cost = calculate_cost(
                model_used,
                usage
            )

            total_cost += turn_cost

            print("\n--- Turn information ---")
            print(f"Turn: {turn_number}")
            print(f"Model: {model_used}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Completion tokens: {completion_tokens}")
            print(f"Total tokens: {total_tokens}")
            print(f"Cached tokens: {cached_tokens}")
            print(f"Cache write tokens: {cache_write_tokens}")
            print(f"Turn cost: ${turn_cost:.8f}")
            print(f"Conversation total cost: ${total_cost:.8f}")

        except Exception as error:

            print(f"\nError: {error}")

            # Remove the user message if the entire turn failed
            messages.pop()


if __name__ == "__main__":
    main()