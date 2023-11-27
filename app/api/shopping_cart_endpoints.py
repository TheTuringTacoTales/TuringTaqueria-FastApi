from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from model.shopping_cart import ShoppingCart, CartItem
from model.product import Product

from security.auth import get_current_user, User

from db.sqlite import engine

router = APIRouter()


# Dependency to get the database session
def get_db():
    with Session(engine) as db:
        yield db

# GET endpoint to retrieve user's cart
@router.get("/cart")
def get_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = db.query(ShoppingCart).filter(ShoppingCart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    return cart.cart_items

# POST endpoint to add an item to the cart
@router.post("/cart")
def add_to_cart(item_details: CartItem, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> CartItem:
    # Check if product exists
    product = db.query(Product).filter(Product.id == item_details.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Get or create cart
    cart = db.query(ShoppingCart).filter(ShoppingCart.user_id == current_user.id).first()
    if not cart:
        cart = ShoppingCart(user_id=current_user.id)
        db.add(cart)
        db.commit()
    
    # Add item to cart
    cart_item = CartItem(cart_id=cart.id, product_id=item_details.product_id, quantity=item_details.quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item

# PUT endpoint to update an item in the cart
@router.put("/cart/{item_id}")
def update_cart_item(item_id: int, item_details: CartItem, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> CartItem:
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart.has(user_id=current_user.id)).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = item_details.quantity
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item

# DELETE endpoint to remove an item from the cart
@router.delete("/cart/{item_id}")
def delete_cart_item(item_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart.has(user_id=current_user.id)).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()

    return {"detail": "Cart item deleted successfully"}
# Add more endpoints as needed...
