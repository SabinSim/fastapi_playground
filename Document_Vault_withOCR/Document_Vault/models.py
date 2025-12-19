from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class UserDocument(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)
    content_type = Column(String)
  
    extracted_text = Column(Text, nullable=True)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
