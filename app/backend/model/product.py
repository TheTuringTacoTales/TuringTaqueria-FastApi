from decimal import Decimal
from pydantic import condecimal
from sqlmodel import Field, SQLModel
import enum


class ProductType(str, enum.Enum):
    TACO = "taco"
    DRINK = "drink"

class Product(SQLModel, table=True):
    __tablename__ = 'products'

    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: Decimal = Field(max_digits=5, decimal_places=2)
    currency: str = Field(default="USD")  
    product_type: ProductType