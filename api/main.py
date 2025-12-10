from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .schemas import AddItem
from .crud import add_item_to_order

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/orders/{order_id}/items")
def add_item(order_id: int, body: AddItem, db: Session = Depends(get_db)):
    add_item_to_order(db, order_id, body.product_id, body.quantity)
    return {"status": "ok"}
