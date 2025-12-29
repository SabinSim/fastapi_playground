from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String)
    max_slots = Column(Integer, default=5)
    commute_time = Column(Integer, default=0)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    user_name = Column(String)
