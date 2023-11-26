from sqlalchemy import create_engine, Column, Integer, Boolean
from sqlalchemy.orm import sessionmaker
from .models import Base, User
from passlib.context import CryptContext

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DBStatus(Base):
    __tablename__ = 'db_status'
    id = Column(Integer, primary_key=True)
    is_initialized = Column(Boolean, default=False)

def init_db():
    with SessionLocal() as session:
        if not session.query(DBStatus).filter_by(is_initialized=True).first():
            create_default_user(session)
            mark_as_initialized(session)

def create_default_user(session):
    hashed_password = pwd_context.hash("password")
    default_user = User(username="admin", email="admin@example.com", hashed_password=hashed_password)
    session.add(default_user)
    session.commit()

def mark_as_initialized(session):
    status = DBStatus(is_initialized=True)
    session.add(status)
    session.commit()
