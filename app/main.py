from fastapi import FastAPI

from db_init import init_db

from api.main_endpoints import router as api_main_router
from api.shopping_cart_endpoints import router as api_cart_router

init_db()

app = FastAPI()

app.include_router(api_main_router)
app.include_router(api_cart_router)