# run with: uvicorn fastapi_test:app --reload
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "sup bitch"}


@app.get("/lol")
async def joker(soup: str = None):
    return {"message": "bruuh", "soup": soup}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


class Item(BaseModel):
    name: str = None
    description: str = None
    price: int = None
    tax: float = None


@app.post("/things/")
async def create_item(thing: Item):
    thing.price = thing.price * 4
    return thing
