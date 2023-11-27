from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from models.models import Product

class CartItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: Optional[int] = Field(default=None, foreign_key="shoppingcart.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int

    product: Product = Relationship(back_populates="cart_items")

class ShoppingCart(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    cart_items: List[CartItem] = Relationship(back_populates="cart")