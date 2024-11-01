from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category_id: int
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdatePrice(BaseModel):
    new_price: float = Field(..., gt=0)

class ProductResponse(ProductBase):
    id: int
    is_available: bool

    model_config = ConfigDict(from_attributes=True)
