from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SellerBase(BaseModel):
    name: str
    rating: Optional[float] = None


class SellerCreate(SellerBase):
    pass


class SellerOut(SellerBase):
    id: UUID

    class Config:
        from_attributes = True

