from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

def get_products(db: Session):
    return db.query(models.ProductDB).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.ProductDB(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_orders(db: Session):
    return db.query(models.OrderDB).all()

def create_order(db: Session, order: schemas.OrderCreate):
    total_price = 0
    order_items = []

    for item in order.items:
        product = db.query(models.ProductDB).filter(models.ProductDB.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        
        total_price += product.price * item.quantity
        order_items.append({"product_id": item.product_id, "quantity": item.quantity})
        
        # Update stock
        product.stock -= item.quantity
        db.add(product)

    db_order = models.OrderDB(total_price=total_price, status="pending")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order_items:
        db_order_item = models.OrderItemDB(order_id=db_order.id, **item)
        db.add(db_order_item)

    db.commit()
    return db_order

def update_order_status(db: Session, order_id: int, status_update: schemas.OrderStatusUpdate):
    db_order = db.query(models.OrderDB).filter(models.OrderDB.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if status_update.status not in ["pending", "completed", "shipped"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'pending', 'completed', or 'shipped'")
    
    db_order.status = status_update.status
    db.commit()
    db.refresh(db_order)
    return db_order

