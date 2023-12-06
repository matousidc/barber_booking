# running database functions from crud.py
from database import SessionLocal, engine
import crud
import models

models.Base.metadata.create_all(bind=engine)

# creates schedule rows in DB
with SessionLocal() as db:
    crud.insert_data(db=db)
