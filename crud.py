# functions to interact with database
from sqlalchemy import text
from sqlalchemy.orm import Session
from uuid import uuid4
import models
import schemas


def test_query(engine):
    with engine.connect() as conn:
        xx = conn.execute(text("SELECT * FROM time_slots;"))
        for x in xx.mappings():
            print(x)


def test_orm(db: Session):
    slots = db.query(models.TimeSlot)
    for slot in slots:
        print(slot.__dict__)


def insert_data(db: Session):
    for i in range(0, 7):
        time_slot = create_time_slot(year=2023, week=48, day=i, booked_slot=False)
        db.add(time_slot)
    db.commit()


def create_time_slot(year: int, week: int, day: int, booked_slot: bool = None, user_id: str = None):
    # Create a new TimeSlot instance
    new_time_slot = models.TimeSlot(week=week, day=day, booked_slot=booked_slot, user_id=user_id, year=year)
    return new_time_slot


def get_user(db: Session):
    return db.query(models.User).first()


def get_week(db: Session, week: int):
    return db.query(models.TimeSlot).filter(models.TimeSlot.week == week).all()


def get_day(db: Session, week: int, day: int):
    return db.query(models.TimeSlot).filter(models.TimeSlot.week == week, models.TimeSlot.day == day).first()


def book_slot(db: Session, time_slot_id: int, email: str) -> models.TimeSlot | None:
    # Query TimeSlot and User from database
    existing_time_slot = db.query(models.TimeSlot).filter(models.TimeSlot.id == time_slot_id).first()
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    # Check if the row exists
    if existing_time_slot:
        if not existing_user:  # if new user, create new row in users table
            existing_user = models.User(id=uuid4().hex, email=email, name=None)
            db.add(existing_user)
        if not existing_time_slot.booked_slot:
            # book that slot
            existing_time_slot.booked_slot = True
            existing_time_slot.user_id = existing_user.id
        else:
            return None
        db.commit()
    return existing_time_slot
