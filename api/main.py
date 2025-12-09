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

    available = row[0]
    if available < data.quantity:
        raise HTTPException(400, "Not enough stock")

    # Проверяем, есть ли товар уже в заказе
    cur.execute("""
        SELECT quantity FROM order_items 
        WHERE order_id=%s AND product_id=%s
    """, (order_id, data.product_id))
    row = cur.fetchone()

    if row:
        new_qty = row[0] + data.quantity
        cur.execute("""
            UPDATE order_items 
            SET quantity=%s 
            WHERE order_id=%s AND product_id=%s
        """, (new_qty, order_id, data.product_id))
    else:
        # взять цену на момент продажи
        cur.execute("SELECT price FROM products WHERE id=%s", (data.product_id,))
        price = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO order_items(order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, data.product_id, data.quantity, price))

    # уменьшить остатки на складе
    cur.execute("""
        UPDATE products 
        SET quantity = quantity - %s 
        WHERE id = %s
    """, (data.quantity, data.product_id))

    return {"status": "ok"}
