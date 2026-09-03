from typing import Literal
from pydantic import BaseModel

# basemodel of message
class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str

#using message for request model
class LLMRequest(BaseModel):
    messages: list[Message]

# this is for return reponse    
class LLMResponse(BaseModel):
    response: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int