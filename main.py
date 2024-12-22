# from fastapi import FastAPI, HTTPException, Depends
# from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
# from pydantic import BaseModel
# from typing import List

# # Database connection
# SQLALCHEMY_DATABASE_URL = "postgresql://ironman@localhost:5433/ecommerce"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# # Database models
# class ProductDB(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String)
#     price = Column(Float)
#     stock = Column(Integer)

# class OrderDB(Base):
#     __tablename__ = "orders"

#     id = Column(Integer, primary_key=True, index=True)
#     total_price = Column(Float)
#     status = Column(String)

# class OrderItemDB(Base):
#     __tablename__ = "order_items"

#     id = Column(Integer, primary_key=True, index=True)
#     order_id = Column(Integer, ForeignKey("orders.id"))
#     product_id = Column(Integer, ForeignKey("products.id"))
#     quantity = Column(Integer)

# # Pydantic models
# class ProductCreate(BaseModel):
#     name: str
#     description: str
#     price: float
#     stock: int

# class Product(ProductCreate):
#     id: int

#     class Config:
#         orm_mode = True

# class OrderItem(BaseModel):
#     product_id: int
#     quantity: int

# class OrderCreate(BaseModel):
#     items: List[OrderItem]

# class Order(BaseModel):
#     id: int
#     total_price: float
#     status: str

#     class Config:
#         orm_mode = True

# class OrderStatusUpdate(BaseModel):
#     status: str

# # Create tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # API endpoints
# @app.get("/products", response_model=List[Product])
# def get_products(db: Session = Depends(get_db)):
#     products = db.query(ProductDB).all()
#     return products

# @app.post("/products", response_model=Product)
# def create_product(product: ProductCreate, db: Session = Depends(get_db)):
#     db_product = ProductDB(**product.dict())
#     db.add(db_product)
#     db.commit()
#     db.refresh(db_product)
#     return db_product

# @app.get("/orders", response_model=List[Order])
# def get_orders(db: Session = Depends(get_db)):
#     orders = db.query(OrderDB).all()
#     return orders

# @app.post("/orders", response_model=Order)
# def create_order(order: OrderCreate, db: Session = Depends(get_db)):
#     total_price = 0
#     order_items = []

#     for item in order.items:
#         product = db.query(ProductDB).filter(ProductDB.id == item.product_id).first()
#         if not product:
#             raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
#         if product.stock < item.quantity:
#             raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        
#         total_price += product.price * item.quantity
#         order_items.append({"product_id": item.product_id, "quantity": item.quantity})
        
#         # Update stock
#         product.stock -= item.quantity
#         db.add(product)

#     db_order = OrderDB(total_price=total_price, status="pending")
#     db.add(db_order)
#     db.commit()
#     db.refresh(db_order)

#     for item in order_items:
#         db_order_item = OrderItemDB(order_id=db_order.id, **item)
#         db.add(db_order_item)

#     db.commit()
#     return db_order

# @app.put("/orders/{order_id}", response_model=Order)
# def update_order_status(order_id: int, status_update: OrderStatusUpdate, db: Session = Depends(get_db)):
#     db_order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
#     if not db_order:
#         raise HTTPException(status_code=404, detail="Order not found")
    
#     if status_update.status not in ["pending", "completed", "shipped"]:
#         raise HTTPException(status_code=400, detail="Invalid status. Must be 'pending' or 'completed'")
    
#     db_order.status = status_update.status
#     db.commit()
#     db.refresh(db_order)
#     return db_order

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

import uvicorn
from app.api import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



