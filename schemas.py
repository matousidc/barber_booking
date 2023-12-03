# Pydantic schemas (models)
from pydantic import BaseModel, EmailStr, PastDate


class UserBase(BaseModel):
    name: str | None
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    created_at: PastDate


class User(UserBase):
    id: str

    class Config:
        orm_mode = True


class TimeSlotBase(BaseModel):
    year: int
    week: int
    day: int
    booked_slot: bool = False

    class Config:
        orm_mode = True


class TimeSlot(TimeSlotBase):
    id: int
    user_id: str

    # updated_at = PastDate

    class Config:
        orm_mode = True
