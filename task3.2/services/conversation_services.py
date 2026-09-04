from sqlalchemy.orm import Session
from sqlalchemy import select

from models.conversations import Conversation
from models.messages import Message


def create_conversation(
    db: Session,
    title: str
):
    conversation = Conversation(title=title)

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def add_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str
):
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message

def get_conversation(
    db: Session,
    conversation_id: int
):
    stmt = (
        select(Conversation, Message)
        .join(
            Message,
            Message.conversation_id == Conversation.id
        )
        .where(Conversation.id == conversation_id)
        .order_by(Message.created_at)
    )

    rows = db.execute(stmt).all()

    if not rows:
        return []

    conversation = rows[0][0]

    return {
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "messages": [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at,
            }
            for _, message in rows
        ]
    }