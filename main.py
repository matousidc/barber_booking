from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from datetime import datetime
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
def root() -> RedirectResponse:
    """Redirects to schedule for current week"""
    week_num = datetime.now().strftime("%W")
    return RedirectResponse(url=f"/schedule/{week_num}")


@app.get("/schedule/{week}", status_code=200)
def fetch_schedule(request: Request, week: int | None = None, db: Session = Depends(get_db)):
    """Fetch schedule for given week"""
    if not week:
        week = datetime.now().strftime("%W")
    schedule = crud.get_week(db=db, week=week)
    if not schedule:
        raise HTTPException(status_code=404, detail="No schedule for chosen week")
    is_booked = ["Booked" if x.booked_slot else "Available" for x in schedule]
    # return jinja template with schedule
    return templates.TemplateResponse(name="schedule.html", context={"request": request, "keyword": is_booked})


@app.get("/user", response_model=schemas.User, status_code=200)
def fetch_user(db: Session = Depends(get_db)):
    user = crud.get_user(db=db)
    return user


@app.put("/book_slot", response_model=schemas.TimeSlot, status_code=200)
def book_slot(time_slot_id: int, email: str, db: Session = Depends(get_db)):
    """User books empty slot, use path example: book_slot/?time_slot_id=0&email=xx@gmail.com"""
    booked_slot = crud.book_slot(db=db, time_slot_id=time_slot_id, email=email)
    if not booked_slot:
        raise HTTPException(status_code=404, detail="Slot booking failed, was probably already taken")
    # send email with confirmation
    return booked_slot
