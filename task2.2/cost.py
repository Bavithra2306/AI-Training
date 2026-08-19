from config import PRIMARY_MODEL, FALLBACK_MODEL


# Prices are USD per 1 million tokens.
#
# Keep these values based on the provider/model
# you actually select in OpenRouter.
#
# For free models, these are 0.0.

PRICING = {
    PRIMARY_MODEL: {
        "input": 1.0,
        "output": 2.0,
        "cache_read": 0.0,
        "cache_write": 0.0,
    },

    FALLBACK_MODEL: {
        "input": 0.8,
        "output": 1.5,
        "cache_read": 0.0,
        "cache_write": 0.0,
    },
}


def get_token_counts(usage):
    """
    Extract normal token counts from the API usage.
    """

    prompt_tokens = usage.get("prompt_tokens", 0)

    completion_tokens = usage.get(
        "completion_tokens",
        0
    )

    total_tokens = usage.get(
        "total_tokens",
        prompt_tokens + completion_tokens
    )

    return (
        prompt_tokens,
        completion_tokens,
        total_tokens
    )


def get_cache_counts(usage):
    """
    Extract prompt caching information.

    The provider may or may not return these fields.
    """

    prompt_details = usage.get(
        "prompt_tokens_details",
        {}
    )

    cached_tokens = prompt_details.get(
        "cached_tokens",
        0
    )

    cache_write_tokens = prompt_details.get(
        "cache_write_tokens",
        0
    )

    return cached_tokens, cache_write_tokens


def calculate_cost(model, usage):
    """
    Calculate the cost of one API request.
    """

    pricing = PRICING.get(model)

    if not pricing:
        return 0.0

    prompt_tokens = usage.get(
        "prompt_tokens",
        0
    )

    completion_tokens = usage.get(
        "completion_tokens",
        0
    )

    cached_tokens, cache_write_tokens = (
        get_cache_counts(usage)
    )

    # Normal input tokens that were NOT served
    # from the cache.
    uncached_input_tokens = max(
        prompt_tokens - cached_tokens,
        0
    )

    input_cost = (
        uncached_input_tokens / 1_000_000
    ) * pricing["input"]

    output_cost = (
        completion_tokens / 1_000_000
    ) * pricing["output"]

    cache_read_cost = (
        cached_tokens / 1_000_000
    ) * pricing["cache_read"]

    cache_write_cost = (
        cache_write_tokens / 1_000_000
    ) * pricing["cache_write"]

    total_cost = (
        input_cost
        + output_cost
        + cache_read_cost
        + cache_write_cost
    )

    return total_cost