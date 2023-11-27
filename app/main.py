from fastapi import FastAPI

from backend.api.main_endpoints import router as api_main_router
from backend.api.shopping_cart_endpoints import router as api_cart_router
import backend.db_init as db

db.init_db()

app = FastAPI()

app.include_router(api_main_router)
app.include_router(api_cart_router)