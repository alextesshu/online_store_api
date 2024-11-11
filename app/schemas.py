from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    category_id: int
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    reserved_quantity: int = Field(0, ge=0)
    is_available: Optional[bool] = None
    
    model_config = ConfigDict(from_attributes=True)

class ProductCreate(ProductBase):
    id: None = None
    is_available: None = None

class ProductUpdatePrice(BaseModel):
    new_price: float = Field(..., gt=0)

class ProductResponse(ProductBase):
    pass
