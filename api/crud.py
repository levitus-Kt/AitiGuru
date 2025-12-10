from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models

def add_item_to_order(db: Session, order_id: int, product_id: int, quantity: int):

    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    if product.quantity < quantity:
        raise HTTPException(400, "Not enough stock")

    order_item = db.query(models.OrderItem).filter(
        models.OrderItem.order_id == order_id,
        models.OrderItem.product_id == product_id
    ).first()

    if order_item:
        order_item.quantity += quantity
    else:
        order_item = models.OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=product.price
        )
        db.add(order_item)

    product.quantity -= quantity
    db.commit()
