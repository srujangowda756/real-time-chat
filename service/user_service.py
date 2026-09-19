from sqlalchemy import select
from sqlalchemy.orm import Session

from core.security import (
    hash_password,
    normalize_username,
)
from model.user import User


def create_user(
    db: Session,
    username: str,
    password: str,
) -> User:
    normalized_username = normalize_username(
        username
    )

    existing_user = db.scalar(
        select(User).where(
            User.username == normalized_username
        )
    )

    if existing_user:
        raise ValueError(
            "Username already exists"
        )

    user = User(
        username=normalized_username,
        password_hash=hash_password(password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_all_users(
    db: Session,
) -> list[User]:
    return list(
        db.scalars(
            select(User)
            .order_by(User.username)
        )
    )


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    return db.scalar(
        select(User).where(
            User.id == user_id
        )
    )


def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:
    normalized_username = normalize_username(
        username
    )

    return db.scalar(
        select(User).where(
            User.username == normalized_username
        )
    )