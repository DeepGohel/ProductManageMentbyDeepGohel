from pydantic import BaseModel, field_validator
from datetime import datetime

class ProductCreate(BaseModel):
    title : str
    description : str
    price : float
    status : str
    category_id : int

    @field_validator("status")
    def validate_status(cls, v:str, values=['active','inactive']):
        if v not in values:
            raise ValueError(f"Status should be only one of {values}")
        return v

class ProductOut(ProductCreate):
    id : int
    created_at : datetime
    updated_at : datetime | None
    category_id : int

class CategoryCreate(BaseModel):
    name : str

class CategoryOut(CategoryCreate):
    id : int