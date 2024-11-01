from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..services.products_service import (
    get_product_list, create_product, update_product_price, 
    reserve_product, cancel_reservation, sell_product,
    start_promotion, get_sold_products, get_product_or_404
)
from ..schemas import ProductCreate, ProductUpdatePrice, ProductResponse
from datetime import date
from typing import Optional
from ..db import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/products/", response_model=list[ProductResponse])
def read_products(
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[int] = None,
    subcategory_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return get_product_list(db, skip=skip, limit=limit, category_id=category_id, subcategory_id=subcategory_id)

@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    return get_product_or_404(db, product_id)

@router.post("/products/", response_model=ProductResponse)
def add_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product_data.model_dump())

@router.patch("/products/{product_id}/price", response_model=ProductResponse)
def change_price(product_id: int, update_data: ProductUpdatePrice, db: Session = Depends(get_db)):
    return update_product_price(db, product_id, update_data.new_price)

@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_or_404(db, product_id)
    db.delete(product)
    db.commit()
    return product

@router.post("/products/{product_id}/reserve", response_model=ProductResponse)
def reserve_item(product_id: int, db: Session = Depends(get_db)):
    return reserve_product(db, product_id)

@router.delete("/products/{product_id}/cancel-reservation", response_model=ProductResponse)
def cancel_item_reservation(product_id: int, db: Session = Depends(get_db)):
    return cancel_reservation(db, product_id)

@router.post("/products/{product_id}/sell", response_model=ProductResponse)
def sell_item(product_id: int, db: Session = Depends(get_db)):
    return sell_product(db, product_id)

@router.patch("/products/{product_id}/start-promotion", response_model=ProductResponse)
def apply_discount(product_id: int, discount: float, db: Session = Depends(get_db)):
    return start_promotion(db, product_id, discount)

@router.get("/products/sold/", response_model=list[ProductResponse])
def get_sold_products_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return get_sold_products(db, start_date=start_date, end_date=end_date, category_id=category_id)