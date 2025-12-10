def test_add_item_to_order(client, db):
    # создаём категории, товары, клиента и заказ
    db.execute("INSERT INTO categories (id, name) VALUES (1, 'TestCat')")
    db.execute("INSERT INTO products (id, name, quantity, price, category_id) VALUES (1, 'Product1', 10, 100, 1)")
    db.execute("INSERT INTO clients (id, name, address) VALUES (1, 'Client1', 'addr')")
    db.execute("INSERT INTO orders (id, client_id) VALUES (1, 1)")
    db.commit()

    # добавляем товар
    response = client.post("/orders/1/items", json={"product_id": 1, "quantity": 3})
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    # проверяем остаток
    qty = db.execute("SELECT quantity FROM products WHERE id=1").fetchone()[0]
    assert qty == 7

    # проверяем создание записи в order_items
    row = db.execute("SELECT quantity FROM order_items WHERE order_id=1 AND product_id=1").fetchone()
    assert row[0] == 3


def test_add_item_not_enough_stock(client, db):
    db.execute("INSERT INTO categories (id, name) VALUES (2, 'TestCat2')")
    db.execute("INSERT INTO products (id, name, quantity, price, category_id) VALUES (2, 'Product2', 1, 100, 2)")
    db.execute("INSERT INTO clients (id, name, address) VALUES (2, 'Client2', 'addr')")
    db.execute("INSERT INTO orders (id, client_id) VALUES (2, 2)")
    db.commit()

    response = client.post("/orders/2/items", json={"product_id": 2, "quantity": 5})
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough stock"
