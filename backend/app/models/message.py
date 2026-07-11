from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room = Column(String, index=True)
    content = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    message_type = Column(String, default="text")
    file_path = Column(String, nullable=True)

