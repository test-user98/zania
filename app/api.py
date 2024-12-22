from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/products/", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.get("/orders/", response_model=List[schemas.Order])
def get_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

@app.put("/orders/{order_id}/", response_model=schemas.Order)
def update_order_status(order_id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    return crud.update_order_status(db, order_id, status_update)

