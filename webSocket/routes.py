from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from core.security import decode_access_token
from database.session import SessionLocal
from service.message_service import (
    create_message,
    get_pending_messages,
    get_user_by_id,
    mark_message_delivered,
)
from webSocket.connection_manager import ConnectionManager


router = APIRouter()

manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
):
    db: Session = SessionLocal()

    # Authenticate user using JWT
    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            await websocket.close(code=1008)
            return

        user_id = int(user_id)

    except (ValueError, TypeError):
        await websocket.close(code=1008)
        return

    except Exception:
        await websocket.close(code=1008)
        return

    # Verify that the authenticated user still exists
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        await websocket.close(code=1008)
        db.close()
        return

    # Connect authenticated user
    await manager.connect(
        str(user_id),
        websocket,
    )

    print("User connected:", user_id)

    try:
        # Send messages that arrived while the user was offline
        pending_messages = get_pending_messages(
            db,
            user_id,
        )

        for message in pending_messages:
            message_data = {
                "id": message.id,
                "user": message.sender_id,
                "receiver": message.receiver_id,
                "message": message.message,
                "created_at": message.created_at.isoformat(),
            }

            await manager.send_to_user(
                str(user_id),
                message_data,
            )

            mark_message_delivered(
                db,
                message,
            )

        # Listen for new messages
        while True:
            data = await websocket.receive_json()

            receiver_id = int(data["receiver"])
            message_text = data["message"]

            print("Sender:", user_id)
            print("Receiver:", receiver_id)
            print("Message:", message_text)

            # Verify receiver exists
            receiver = get_user_by_id(
                db,
                receiver_id,
            )

            if receiver is None:
                await manager.send_to_user(
                    str(user_id),
                    {
                        "error": "Receiver does not exist",
                    },
                )
                continue

            # Save message in database
            new_message = create_message(
                db,
                sender_id=user_id,
                receiver_id=receiver_id,
                message=message_text,
            )

            message_data = {
                "id": new_message.id,
                "user": new_message.sender_id,
                "receiver": new_message.receiver_id,
                "message": new_message.message,
                "created_at": new_message.created_at.isoformat(),
            }

            # Deliver immediately if receiver is online
            if manager.is_connected(str(receiver_id)):
                await manager.send_to_user(
                    str(receiver_id),
                    message_data,
                )

                mark_message_delivered(
                    db,
                    new_message,
                )

            # Send message back to sender
            await manager.send_to_user(
                str(user_id),
                message_data,
            )

    except WebSocketDisconnect:
        manager.disconnect(str(user_id))

        print("User disconnected:", user_id)

    except Exception as error:
        print("WebSocket error:", error)

        manager.disconnect(str(user_id))

    finally:
        db.close()