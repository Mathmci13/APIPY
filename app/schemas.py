from pydantic import BaseModel
from typing import Optional

# Schema para criação de um produto
class ProductCreate(BaseModel):
    name: str
    price: int
    quantity: int
    description: Optional[str] = None


class Product(ProductCreate):
    id: int

    class Config:
        orm_mode = True
