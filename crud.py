# functions to interact with database
from datetime import datetime
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


def insert_timeslots(db: Session):
    """Create timeslots in database"""
    week_num = int(datetime.now().strftime("%W"))
    for x in range(0, 5):
        for i in range(0, 7):
            time_slot = create_time_slot(year=2024, week=week_num + x, day=i, booked_slot=False)
            db.add(time_slot)
    db.commit()


def create_time_slot(year: int, week: int, day: int, booked_slot: bool = None, user_id: str = None) -> models.TimeSlot:
    return models.TimeSlot(week=week, day=day, booked_slot=booked_slot, user_id=user_id, year=year)


def get_user(db: Session) -> models.User | None:
    return db.query(models.User).first()


def get_week(db: Session, week: int) -> list[models.TimeSlot]:
    return db.query(models.TimeSlot).filter(models.TimeSlot.week == week).all()


def get_day(db: Session, time_slot: schemas.TimeSlotBase) -> models.TimeSlot | None:
    return db.query(models.TimeSlot).filter(models.TimeSlot.week == time_slot.week,
                                            models.TimeSlot.day == time_slot.day).first()


def book_slot(db: Session, time_slot_id: int, user: schemas.UserBase) -> models.TimeSlot | None:
    # Query TimeSlot and User from database
    existing_time_slot = db.query(models.TimeSlot).filter(models.TimeSlot.id == time_slot_id).first()
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    # Check if the row exists
    if existing_time_slot:
        if not existing_user:  # if new user, create new row in users table
            existing_user = models.User(**user.dict(), id=uuid4().hex)
            db.add(existing_user)
        else:  # user could have chosen new name, update in db
            if existing_user.name != user.name:
                existing_user.name = user.name
                db.add(existing_user)
        if not existing_time_slot.booked_slot:
            # book that slot
            existing_time_slot.booked_slot = True
            existing_time_slot.user_id = existing_user.id
        else:
            return None
        db.commit()
    return existing_time_slot
