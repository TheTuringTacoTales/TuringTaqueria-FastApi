from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from .product import Product

class CartItem(SQLModel, table=True):
    __tablename__ = 'cart_items'

    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: Optional[int] = Field(default=None, foreign_key="shopping_carts.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int
    
    product: Product = Relationship(sa_relationship_kwargs=dict(lazy="joined"))
    cart: "ShoppingCart" = Relationship()

class ShoppingCart(SQLModel, table=True):
    __tablename__ = 'shopping_carts'

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    cart_items: List[CartItem] = Relationship(back_populates="cart", sa_relationship_kwargs=dict(lazy="joined"))
