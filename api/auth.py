from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.security import get_current_user
from database.session import get_db
from model.user import User
from schema.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
)
from schema.user import UserResponse
from service.auth_service import (
    authenticate_user,
    register_user,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    return register_user(
        db,
        data,
    )


@router.post(
    "/login",
    response_model=AuthResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    access_token = authenticate_user(
        db,
        data,
    )

    return AuthResponse(
        access_token=access_token,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user