from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import Optional

class Username(str):
    pass

class Password(str):
    pass

class HashedPassword(str):
    pass

class AuthToken(BaseModel):
    access_token: str
    token_type: str

class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str 
    email: str = Field(unique=True, index=True)
    hashed_password: HashedPassword
