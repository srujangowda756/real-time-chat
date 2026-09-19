from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.security import get_current_user
from database.session import get_db
from model.user import User
from schema.user import UserResponse
from service.user_service import get_all_users


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    users = get_all_users(db)

    return [
        user
        for user in users
        if user.id != current_user.id
    ]