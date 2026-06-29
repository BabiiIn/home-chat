# from sqlalchemy.orm import Session
# from app.models.message import Message

# def save_message(
#     db: Session,
#     user_id: int,
#     room: str,
#     content: str | None,
#     message_type: str,
#     file_path: str | None
# ):
#     msg = Message(
#         user_id=user_id,
#         room=room,
#         content=content,

#     )
#     db.add(msg)
#     db.commit()
#     db.refresh(msg)
#     return msg

# def get_last_messages(db: Session, room: str, limit: int = 20):
#     return (
#         db.query(Message)
#         .filter(Message.room == room)
#         .order_by(Message.timestamp.desc())
#         .limit(limit)
#         .all()
#     )

from sqlalchemy.orm import Session
from app.models.message import Message

def save_message(
    db: Session,
    user_id: int,
    room: str,
    content: str | None,
    message_type: str,
    file_path: str | None
):
    msg = Message(
        user_id=user_id,
        room=room,
        content=content,
        message_type=message_type,
        file_path=file_path
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_last_messages(db: Session, room: str, limit: int = 20):
    return (
        db.query(Message)
        .filter(Message.room == room)
        .order_by(Message.timestamp.desc())
        .limit(limit)
        .all()
)