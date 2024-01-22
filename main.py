# run with: uvicorn main:app --reload
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud
import models
import schemas
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
def root() -> RedirectResponse:
    """Redirects to schedule for current week"""
    week_num = datetime.now().strftime("%W")
    return RedirectResponse(url=f"/schedule/{week_num}")


@app.get("/schedule/{week}", status_code=200)
def fetch_schedule(request: Request, week: int | None = None, db: Session = Depends(get_db)):
    """Fetch schedule for given week, returns jinja template with schedule"""
    if not week:
        week = datetime.now().strftime("%W")
    schedule = crud.get_week(db=db, week=week)
    if not schedule:
        raise HTTPException(status_code=404, detail="No schedule for chosen week")
    is_booked = ["Booked" if x.booked_slot else "Available" for x in schedule]
    return templates.TemplateResponse(name="schedule.html", context={"request": request, "keyword": is_booked})


@app.get("/user", response_model=schemas.User, status_code=200)
def fetch_user(db: Session = Depends(get_db)):
    user = crud.get_user(db=db)
    return user


@app.put("/book_slot", response_model=schemas.TimeSlot, status_code=200)
def book_slot(time_slot_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    """User books empty slot, use path example: book_slot/?time_slot_id=0 + body"""
    booked_slot = crud.book_slot(db=db, time_slot_id=time_slot_id, user=user)
    if not booked_slot:
        raise HTTPException(status_code=404, detail="Slot booking failed, was probably already taken")
    # send email with confirmation
    return booked_slot


@app.put("/book_slot_test", response_model=schemas.TimeSlot, status_code=200)
def book_slot_test(time_slot_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    """Test endpoint for speed of database """
    # booked_slot = crud.book_slot(db=db, time_slot_id=time_slot_id, user=user)
    booked_slot = models.TimeSlot(id=555, week=5, day=1, year=2024, user_id='ssf', booked_slot=True)
    if not booked_slot:
        raise HTTPException(status_code=404, detail="Slot booking failed, was probably already taken")
    # send email with confirmation
    return booked_slot
