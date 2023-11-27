from sqlmodel import Field, SQLModel, Session, create_engine
from security.model import User
from model.product import Product, ProductType
from passlib.context import CryptContext

from db.sqlite import engine, create_db_and_tables

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DBStatus(SQLModel, table=True):
    __tablename__ = 'db_status'
    id: int = Field(primary_key=True)
    is_initialized: bool = Field(default=False)

def init_db():
    create_db_and_tables()
    with Session(engine) as session: # type: ignore
        if not session.query(DBStatus).filter_by(is_initialized=True).first():
            create_default_user(session)
            create_sample_products(session)
            mark_as_initialized(session)

def mark_as_initialized(session: Session):
    status = DBStatus(is_initialized=True)
    session.add(status)
    session.commit()

def create_default_user(session: Session):
    hashed_password = pwd_context.hash("password")
    default_user = User(username="admin", email="admin@example.com", hashed_password=hashed_password)
    session.add(default_user)
    session.commit()

def create_sample_products(session: Session):
    sample_products = [
        Product(name="Classic Taco", price=2.5, product_type=ProductType.TACO),
        Product(name="Fish Taco", price=3.0, product_type=ProductType.TACO),
        Product(name="Carne Asada Taco", price=3.5, product_type=ProductType.TACO),
        Product(name="Al Pastor Taco", price=3.0, product_type=ProductType.TACO),
        Product(name="Chorizo Taco", price=2.8, product_type=ProductType.TACO),
        Product(name="Lemonade", price=1.0, product_type=ProductType.DRINK),
        Product(name="Margarita", price=4.0, product_type=ProductType.DRINK),
        Product(name="Horchata", price=1.5, product_type=ProductType.DRINK),
        Product(name="Agua Fresca", price=1.2, product_type=ProductType.DRINK),
        Product(name="Mexican Coke", price=1.5, product_type=ProductType.DRINK)
    ]
    session.add_all(sample_products)
    session.commit()