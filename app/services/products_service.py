from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..db import models
from ..schemas import ProductCreate
from datetime import date
from typing import Optional

def get_product_list(db: Session, skip: int = 0, limit: int = 10, category_id: int = None, subcategory_id: int = None):
    query = db.query(models.Product)

    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if subcategory_id:
        query = query.filter(models.Product.subcategory_id == subcategory_id)

    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product_data: dict):
    product = models.Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product_price(db: Session, product_id: int, new_price: float):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        product.price = new_price
        db.commit()
        db.refresh(product)
    return product

def reserve_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock <= 0:
        raise HTTPException(status_code=400, detail="Product is out of stock")
    
    product.stock -= 1
    db.commit()
    db.refresh(product)
    return product

def cancel_reservation(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    product.stock += 1
    db.commit()
    db.refresh(product)
    return product

def sell_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None or product.stock <= 0:
        raise HTTPException(status_code=400, detail="Product not available for sale")
    
    product.stock -= 1
    if product.stock == 0:
        product.is_available = False
    product.sold_date = date.today()
    db.commit()
    db.refresh(product)
    return product

def start_promotion(db: Session, product_id: int, discount: float):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if discount < 0 or discount > 100:
        raise HTTPException(status_code=400, detail="Discount must be between 0 and 100")
    
    product.discount = discount
    product.price = product.price * (1 - discount / 100)
    db.commit()
    db.refresh(product)
    return product

def get_sold_products(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None, category_id: Optional[int] = None):
    query = db.query(models.Product).filter(models.Product.is_available == False)

    if start_date:
        query = query.filter(models.Product.sold_date >= start_date)
    if end_date:
        query = query.filter(models.Product.sold_date <= end_date)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    
    return query.all()