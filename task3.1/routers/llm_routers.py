from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from schemas import LLMRequest, LLMResponse
from services.llm_service import call_llm
from services.llm_service import call_llm, stream_llm

router = APIRouter(
    prefix="/llm",
    tags=["LLM"]
)


@router.post(
    "/generate",
    response_model=LLMResponse
)
async def generate_response(request: LLMRequest, http_request: Request):
    request_id = http_request.state.request_id
    return await call_llm(request, request_id)



@router.post("/stream")
async def stream_response(request: LLMRequest):

    return StreamingResponse(
        stream_llm(request),
        media_type="text/event-stream"
    )