from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import User
from .db_init import SessionLocal
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "5baef34f54e530634f94f677563570879716fcf0c0dcf0c44b9510a81e1d74bf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Username(str):
    pass

class Password(str):
    pass

class HashedPassword(str):
    pass

class AuthToken(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password: Password, hashed_password: HashedPassword):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: Password):
    return pwd_context.hash(password)

def get_user(db: Session, username: Username) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: Username, password: Password) -> Optional[User]:
    user = get_user(db, username)
    if not user:
        return None
    if not verify_password(password, HashedPassword(user.hashed_password)):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> AuthToken:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return AuthToken(access_token=encoded_jwt, token_type="bearer")

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[Username] = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    with SessionLocal() as db:
        user = get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user
