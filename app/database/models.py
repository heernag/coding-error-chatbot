from sqlalchemy import Column, Integer, String, Text, DateTime, Identity
from datetime import datetime
from app.database.connection import Base

class ChatHistory(Base):
    __tablename__ = 'chat_history'

    
    id = Column(Integer, Identity(start=1), primary_key = True)
    session_id = Column(String(50), index=True, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    