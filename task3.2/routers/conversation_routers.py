from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schemas import ConversationCreate, MessageCreate
from services.conversation_services import (
    create_conversation,
    add_message,
    get_conversation
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.post("/create")
def create_new_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db)
):
    return create_conversation(
        db,
        data.title
    )


@router.post("/{conversation_id}/messages")
def create_new_message(
    conversation_id: int,
    data: MessageCreate,
    db: Session = Depends(get_db)
):
    return add_message(
        db,
        conversation_id,
        data.role,
        data.content
    )
    
@router.get("/{conversation_id}")
def replay_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    return get_conversation(
        db,
        conversation_id
    )