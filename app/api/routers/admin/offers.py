from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models import Offer, Product, Seller
from app.schemas.offer import OfferCreate, OfferOut, OfferUpdate


router = APIRouter(
    prefix="/v1/admin",
    tags=["admin:offers"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/products/{product_id}/offers", response_model=List[OfferOut])
async def list_product_offers(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[OfferOut]:
    result = await db.execute(select(Offer).where(Offer.product_id == product_id))
    offers = result.scalars().all()
    return [OfferOut.model_validate(o) for o in offers]


@router.post(
    "/products/{product_id}/offers",
    response_model=OfferOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_offer_for_product(
    product_id: UUID,
    data: OfferCreate,
    db: AsyncSession = Depends(get_db),
) -> OfferOut:
    # Ensure product and seller exist
    product_result = await db.execute(select(Product).where(Product.id == product_id))
    if product_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    seller_result = await db.execute(select(Seller).where(Seller.id == data.seller_id))
    if seller_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")

    offer = Offer(
        product_id=product_id,
        seller_id=data.seller_id,
        price_amount=data.price_amount,
        price_currency=data.price_currency,
        delivery_date=data.delivery_date,
    )
    db.add(offer)
    await db.commit()
    await db.refresh(offer)
    return OfferOut.model_validate(offer)


@router.put("/offers/{offer_id}", response_model=OfferOut)
async def update_offer(
    offer_id: UUID,
    data: OfferUpdate,
    db: AsyncSession = Depends(get_db),
) -> OfferOut:
    result = await db.execute(select(Offer).where(Offer.id == offer_id))
    offer = result.scalar_one_or_none()
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")

    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(offer, field, value)

    await db.commit()
    await db.refresh(offer)
    return OfferOut.model_validate(offer)


@router.delete("/offers/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offer(
    offer_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(select(Offer).where(Offer.id == offer_id))
    offer = result.scalar_one_or_none()
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")

    await db.delete(offer)
    await db.commit()

