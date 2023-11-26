from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User
from models.db_init import init_db
from models.auth import Username, Password, authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Initialize the DB
init_db()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to TuringTaqueriaApi!"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with SessionLocal() as db:
        user = authenticate_user(db, Username(form_data.username), Password(form_data.password))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        auth_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": auth_token.access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user