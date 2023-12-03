# run with: uvicorn fastapi_main:app --reload
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Serve static files (e.g., CSS, JS) from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Use Jinja2 for HTML templates
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/bruh")
def read_bruh(request: Request):
    return templates.TemplateResponse("bruh.html", {"request": request, "keyword": "loooooooooool"})
