from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.session import get_db
from schema.message import MessageResponse
from service.message_service import get_pending_messages


router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/pending/{receiver_id}", response_model=list[MessageResponse])
def pending_messages(
    receiver_id: int,
    db: Session = Depends(get_db),
) -> list[MessageResponse]:
    return get_pending_messages(db, receiver_id)