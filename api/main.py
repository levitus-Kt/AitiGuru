from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    dbname="shop",
    user="postgres",
    password="postgres",
    host="localhost"
)
conn.autocommit = True

class AddItem(BaseModel):
    product_id: int
    quantity: int

@app.post("/orders/{order_id}/items")
def add_item(order_id: int, data: AddItem):
    cur = conn.cursor()

    # Проверить наличие товара
    cur.execute("SELECT quantity FROM products WHERE id=%s", (data.product_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(404, "Product not found")


    return {"status": "ok"}
