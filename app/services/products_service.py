from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..db import models
from datetime import date
from typing import Optional, List

def get_product_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[int] = None,
    subcategory_id: Optional[int] = None
    
) -> List[models.Product]:
    query = db.query(models.Product)

    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)
    if subcategory_id is not None:
        query = query.filter(models.Product.subcategory_id == subcategory_id)

    return query.offset(skip).limit(limit).all()

def get_product_or_404(db: Session, product_id: int) -> models.Product:
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

def create_product(db: Session, product_data: dict) -> models.Product:
    product = models.Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product_price(db: Session, product_id: int, new_price: float) -> Optional[models.Product]:
    product = get_product_or_404(db, product_id)
    product.price = new_price
    db.commit()
    db.refresh(product)
    return product

def reserve_product(db: Session, product_id: int) -> models.Product:
    product = get_product_or_404(db, product_id)
    if product.stock <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product is out of stock")
    product.stock -= 1
    db.commit()
    db.refresh(product)
    return product

def cancel_reservation(db: Session, product_id: int) -> models.Product:
    product = get_product_or_404(db, product_id)
    product.stock += 1
    db.commit()
    db.refresh(product)
    return product

def sell_product(db: Session, product_id: int) -> models.Product:
    product = get_product_or_404(db, product_id)
    if product.stock <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product not available for sale")
    product.stock -= 1
    if product.stock == 0:
        product.is_available = False
    product.sold_date = date.today()
    db.commit()
    db.refresh(product)
    return product

def start_promotion(db: Session, product_id: int, discount: float) -> models.Product:
    if not (0 <= discount <= 100):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Discount must be between 0 and 100")
    product = get_product_or_404(db, product_id)
    product.discount = discount
    product.price *= (1 - discount / 100)
    db.commit()
    db.refresh(product)
    return product

def get_sold_products(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None
) -> List[models.Product]:
    query = db.query(models.Product).filter(models.Product.is_available == False)

    if start_date:
        query = query.filter(models.Product.sold_date >= start_date)
    if end_date:
        query = query.filter(models.Product.sold_date <= end_date)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    
    return query.all()