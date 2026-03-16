from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProductAttributeIn(BaseModel):
    key: str
    value: str


class ProductBase(BaseModel):
    name: str
    price_amount: float
    price_currency: str
    stock: int = 0
    image_object_key: Optional[str] = None
    thumbnail_object_key: Optional[str] = None
    attributes: List[ProductAttributeIn] = Field(default_factory=list)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price_amount: Optional[float] = None
    price_currency: Optional[str] = None
    stock: Optional[int] = None
    image_object_key: Optional[str] = None
    thumbnail_object_key: Optional[str] = None
    attributes: Optional[List[ProductAttributeIn]] = None


class ProductOut(BaseModel):
    id: UUID
    name: str
    price_amount: float
    price_currency: str
    stock: int
    image_object_key: Optional[str]
    thumbnail_object_key: Optional[str]
    attributes: List[ProductAttributeIn]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

