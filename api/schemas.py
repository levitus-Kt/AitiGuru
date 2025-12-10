from pydantic import BaseModel

class AddItem(BaseModel):
    product_id: int
    quantity: int
