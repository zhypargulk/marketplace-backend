from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models import Seller
from app.schemas.seller import SellerCreate, SellerOut


router = APIRouter(
    prefix="/v1/admin/sellers",
    tags=["admin:sellers"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("", response_model=List[SellerOut])
async def list_sellers(db: AsyncSession = Depends(get_db)) -> List[SellerOut]:
    result = await db.execute(select(Seller))
    sellers = result.scalars().all()
    return [SellerOut.model_validate(s) for s in sellers]


@router.post("", response_model=SellerOut, status_code=status.HTTP_201_CREATED)
async def create_seller(
    data: SellerCreate,
    db: AsyncSession = Depends(get_db),
) -> SellerOut:
    seller = Seller(name=data.name, rating=data.rating)
    db.add(seller)
    await db.commit()
    await db.refresh(seller)
    return SellerOut.model_validate(seller)

