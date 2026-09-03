import asyncio
from openai import (
    AsyncOpenAI,
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
)
import time
import json
import logging

from config import settings
from schemas import LLMRequest, LLMResponse

logger =logging.getLogger(__name__)

client = AsyncOpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)
# a dict to store cache
cache = {}

#to create cache key...
def create_cache_key(request: LLMRequest) -> str:
    return json.dumps(
        {
            "messages": [
                message.model_dump()
                for message in request.messages
            ],
            "model": settings.LLM_MODEL,
            "temperature": settings.LLM_TEMPERATURE,
        },
        sort_keys=True
    )

#-------------------------#
#.....For Calling LLM.....#
#-------------------------#
async def call_llm(request: LLMRequest, request_id: str) -> LLMResponse:
    logger.info(
    "LLM request started | request_id=%s",
    request_id
)
    # calling cache_key func
    cache_key = create_cache_key(request)
    
    if cache_key in cache:
        cached_response, cached_time = cache[cache_key]

        if time.time() - cached_time < settings.LLM_CACHE_TTL:
            print("CACHE HIT")
            return cached_response
    for attempt in range(settings.LLM_MAX_RETRIES):

        try:
            response = await client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    message.model_dump()
                    for message in request.messages
                ],
                temperature=settings.LLM_TEMPERATURE,
                timeout=settings.LLM_TIMEOUT,
            )

            content = response.choices[0].message.content or ""
            print("RESPONSE:", response)
            usage = response.usage

            input_tokens = usage.prompt_tokens if usage else 0
            output_tokens = usage.completion_tokens if usage else 0
            total_tokens = usage.total_tokens if usage else 0

            
            result = LLMResponse(
            response=content,
            model=response.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            )  
            
            logger.info(
                "LLM request completed | request_id=%s | model=%s | input_tokens=%s | output_tokens=%s",
                request_id,
                response.model,
                input_tokens,
                output_tokens,
            )
            cache[cache_key] = (result, time.time())
            return result
        
        except (
            RateLimitError,
            APITimeoutError,
            APIConnectionError,
        ):

            if attempt == settings.LLM_MAX_RETRIES - 1:
                raise

            await asyncio.sleep(2 ** attempt)
#-------------------------#
#......For Streaming......#
#-------------------------#
    
async def stream_llm(request: LLMRequest):

    stream = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            message.model_dump()
            for message in request.messages
        ],
        temperature=settings.LLM_TEMPERATURE,
        stream=True,
    )

    async for chunk in stream:

        if not chunk.choices:
            continue

        content = chunk.choices[0].delta.content

        if content:
            yield content