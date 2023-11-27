from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


from fastapi.staticfiles import StaticFiles

def configure_static(app):
    app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/restaurant")
def get_login(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})    