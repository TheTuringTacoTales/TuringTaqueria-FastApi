from fastapi import FastAPI

app = FastAPI()

# Setup the back end
from backend.api.main_endpoints import router as api_main_router
from backend.api.shopping_cart_endpoints import router as api_cart_router
import backend.db_init as db

db.init_db()
app.include_router(api_main_router)
app.include_router(api_cart_router)

# Setup the front end
from frontend import router as frontend_router
from frontend import configure_static
app.include_router(frontend_router)
configure_static(app)
