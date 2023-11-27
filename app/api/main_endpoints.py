from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List

from model.product import Product
from security.model import User, Username, Password
from security.auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

from db.sqlite import engine

router = APIRouter()


# Dependency to get the database session
def get_db():
    with Session(engine) as db: # type: ignore
        yield db


@router.get("/")
async def root():
    return {"message": "Welcome to TuringTaqueriaApi!"}

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user

@router.get("/products", response_model=list[Product]) 
def read_products(current_user: User = Security(get_current_user), db: Session = Depends(get_db)) -> List[Product]:
    products = db.query(Product).all()
    return products

@router.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
