from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.security import (
    create_access_token,
    hash_password,
    normalize_username,
    verify_password,
)
from model.user import User
from schema.auth import LoginRequest, RegisterRequest


def register_user(
    db: Session,
    data: RegisterRequest,
) -> User:
    username = normalize_username(
        data.username
    )

    existing_user = db.scalar(
        select(User).where(
            User.username == username
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    user = User(
        username=username,
        password_hash=hash_password(
            data.password
        ),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    data: LoginRequest,
) -> str:
    username = normalize_username(
        data.username
    )

    user = db.scalar(
        select(User).where(
            User.username == username
        )
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return create_access_token(
        user.id
    )