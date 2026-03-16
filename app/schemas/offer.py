from __future__ import annotations

from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class OfferBase(BaseModel):
    price_amount: float
    price_currency: str
    delivery_date: Optional[date] = None


class OfferCreate(OfferBase):
    seller_id: UUID


class OfferUpdate(BaseModel):
    price_amount: Optional[float] = None
    price_currency: Optional[str] = None
    delivery_date: Optional[date] = None


class OfferOut(OfferBase):
    id: UUID
    product_id: UUID
    seller_id: UUID

    class Config:
        from_attributes = True

