from pydantic import BaseModel
from typing import List

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class Product(ProductCreate):
    id: int

    class Config:
        orm_mode = True

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItem]

class Order(BaseModel):
    id: int
    total_price: float
    status: str

    class Config:
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    status: str

