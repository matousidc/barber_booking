# SQLAlchemy defined DB models (tables)
from sqlalchemy import Boolean, Column, Integer, String, Index
from database import Base


class TimeSlot(Base):
    __tablename__ = 'time_slots'
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    week = Column(Integer, index=True)
    day = Column(Integer, index=True)
    booked_slot = Column(Boolean, default=False)
    user_id = Column(String(255), nullable=True, default=None)
    user_id_idx = Index('user_id_idx', 'user_id')


class User(Base):
    __tablename__ = "users"
    id = Column(String(255), primary_key=True, index=True, nullable=True, unique=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
