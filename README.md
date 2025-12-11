# AitiGuru

Микросервис для управления товарами и заказами.

Поддерживает хранение номенклатуры, категорий с неограниченной вложенностью, клиентов и заказов.

Реализован REST-метод «Добавление товара в заказ».

## Функциональность

✔ Хранение номенклатуры (товары, количество, цена)

✔ Дерево категорий товаров с бесконечной вложенностью

✔ Клиенты и заказы

✔ Таблица позиций заказа

✔ REST-метод: добавление товара в заказ

✔ Увеличение количества, если товар уже есть в заказе

✔ Проверка наличия товара на складе

✔ Контейнеризация (Docker + Docker Compose)

✔ Автоматические миграции БД (Alembic)

✔ Автотесты с pytest

✔ GitHub Actions CI для запуска автотестов

## Технологический стек

Python 3.11

FastAPI

PostgreSQL 15

SQLAlchemy

Alembic

Docker / Docker Compose

Pytest

Uvicorn

## Структура проекта

```
project/
│
├── sql/
│   ├── count_child.txt
│   ├── optimization.txt
│   ├── orders_sum.txt
│   ├── view_top5.txt
│   └── tables/
│       ├── categories.txt
│       ├── clients.txt
│       ├── orders.txt
│       ├── products.txt
│       └── order_items.txt
│
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── alembic.ini
│   ├── migrations/
│   │   └── versions/
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       └── test_add_item.py
│
├── docker-compose.yml
└── .github/
    └── workflows/
        └── ci.yml
```

## SQL

В папке sql хранятся запросы к таблицам в папке sql/tables

count_child - подсчет дочерних категорий

orders_sum - сумма заказов по клиенту

optimization - оптимизированные запросы

# Запуск сервиса

1. Установить Docker и Docker Compose

https://docs.docker.com/get-docker/

2. Запустить проект

docker-compose up --build

3. Проверить работу API

Swagger UI доступен по адресу: http://localhost:8000/docs

### REST-методы

➕ Добавление товара в заказ

```POST /orders/{order_id}/items```


Тело запроса:

```
{
  "product_id": 1,
  "quantity": 3
}
```

Логика:

если товар есть в заказе → увеличиваем количество

если товара нет в заказе → создаём новую строку

если товара нет на складе → ошибка 400

Пример ответа:

```
{
  "status": "ok"
}
```

## Структура БД

Основные таблицы:

categories — дерево категорий (Adjacency List)

products — номенклатура

clients — клиенты

orders — заказы клиентов

order_items — состав заказа

## Автотесты

Тесты находятся в api/tests/ и используют:

pytest

FastAPI TestClient

тестовую SQLite БД

Запуск локально:

```cd api```

```pytest -vv```
