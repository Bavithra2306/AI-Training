from datetime import datetime
from pydantic import BaseModel


class ConversationCreate(BaseModel):
    title: str


class MessageCreate(BaseModel):
    role: str
    content: str


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: list[MessageResponse]

    model_config = {
        "from_attributes": True
    }