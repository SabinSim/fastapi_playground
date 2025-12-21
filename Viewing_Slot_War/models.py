from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Property(Base):
    # [KOR] 매물 정보 테이블
    # [ENG] Property Information Table
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    # [KOR] 최대 예약 가능 인원 (이 규칙을 지키는 것이 핵심)
    # [ENG] Maximum capacity (Crucial to strictly enforce this limit)
    max_slots = Column(Integer)

class Booking(Base):
    # [KOR] 예약 기록 테이블
    # [ENG] Booking History Table
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    
    # [KOR] 예약자 이름 (식별자)
    # [ENG] Booker's Name (Identifier)
    user_name = Column(String)