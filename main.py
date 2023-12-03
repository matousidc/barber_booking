from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", status_code=200)
def root(request: Request):
    return templates.TemplateResponse(name="barber_index.html", context={"request": request})


@app.get("/schedule/{week}", response_model=list[schemas.TimeSlotBase], status_code=200)
def fetch_schedule(week: int | None = None, db: Session = Depends(get_db)):
    """Fetch schedule for given week"""
    if not week:
        week = 48
    schedule = crud.get_week(db=db, week=week)
    if not schedule:
        raise HTTPException(status_code=404, detail="No schedule for chosen week")
    # return jinja template with schedule
    return schedule


@app.get("/schedule/day/{day}", response_model=schemas.TimeSlotBase, status_code=200)
def fetch_schedule_day(day: int | None = None, db: Session = Depends(get_db)):
    """Fetch schedule for given week"""
    week = 48
    schedule = crud.get_day(db=db, week=week, day=day)
    if not schedule:
        raise HTTPException(status_code=404, detail="No schedule for chosen week")
    return schedule


@app.get("/user", response_model=schemas.User, status_code=200)
def fetch_user(db: Session = Depends(get_db)):
    user = crud.get_user(db=db)
    return user


@app.put("/book_slot", response_model=schemas.TimeSlot, status_code=200)
def book_slot(time_slot_id: int, email: str, db: Session = Depends(get_db)):
    """User books empty slot, use path example: book_slot/?time_slot_id=0&email=xx@gmail.com"""
    # DB write query, change from empty to booked, validate if slot was really empty
    booked_slot = crud.book_slot(db=db, time_slot_id=time_slot_id, email=email)
    if not booked_slot:
        raise HTTPException(status_code=404, detail="Slot not booked, was probably already taken")
    # send email with confirmation
    return booked_slot
    # return crud.book_slot(db=db, time_slot_id=time_slot_id, email=email)
