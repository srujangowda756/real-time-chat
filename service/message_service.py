from sqlalchemy import select
from sqlalchemy.orm import Session

from model.message import Message
from model.user import User


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    return db.scalar(
        select(User).where(User.id == user_id)
    )


def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:
    return db.scalar(
        select(User).where(User.username == username)
    )


def create_message(
    db: Session,
    sender_id: int,
    receiver_id: int,
    message: str,
) -> Message:
    new_message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        message=message,
        delivered=False,
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


def get_pending_messages(
    db: Session,
    receiver_id: int,
) -> list[Message]:
    return list(
        db.scalars(
            select(Message)
            .where(
                Message.receiver_id == receiver_id,
                Message.delivered.is_(False),
            )
            .order_by(Message.created_at)
        )
    )


def mark_message_delivered(
    db: Session,
    message: Message,
) -> None:
    message.delivered = True
    db.commit()