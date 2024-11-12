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
    if product.stock - product.reserved_quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product is out of stock")
    product.reserved_quantity += 1
    db.commit()
    db.refresh(product)
    return product

def cancel_reservation(db: Session, product_id: int) -> models.Product:
    product = get_product_or_404(db, product_id)
    if product.reserved_quantity > 0:
        product.reserved_quantity -= 1
    db.commit()
    db.refresh(product)
    return product

def sell_product(db: Session, product_id: int) -> models.Product:
    product = get_product_or_404(db, product_id)

    if product.reserved_quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product not available for sale")

    # Применение скидки
    discounted_price = apply_discount(db, product_id)
    sale = models.Sale(
        product_id=product_id,
        actual_price=product.price,
        discounted_price=discounted_price,
        sale_date=date.today()
    )

    product.reserved_quantity -= 1
    product.stock -= 1

    if product.stock == 0:
        product.is_available = False
        product.sold_date = date.today()

    db.add(sale)
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

def apply_discount(db: Session, product_id: int) -> float:
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise ValueError("Product not found")
    
    discount_value = 0.0
    discounts = db.query(models.Discount).filter(
        (models.Discount.product_id == product_id) |
        (models.Discount.category_id == product.category_id) |
        (models.Discount.subcategory_id == product.subcategory_id)
    ).all()
    
    if discounts:
        discount_value = max(discount.percentage for discount in discounts)
    
    discounted_price = product.price * (1 - discount_value / 100)
    return discounted_price