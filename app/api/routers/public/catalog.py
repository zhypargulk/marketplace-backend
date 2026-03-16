from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Offer, Product, Seller
from app.storage.minio_client import get_product_image


router = APIRouter(prefix="/v1/public/products", tags=["public:products"])

# 1x1 transparent GIF so "no image" still returns a valid image
_PLACEHOLDER_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00"
    b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


@router.get("")
async def list_products(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(
            Product.id,
            Product.name,
            Product.thumbnail_object_key,
            func.min(Offer.price_amount).label("price_amount"),
            Product.stock,
            func.min(Offer.delivery_date).label("nearest_delivery_date"),
        )
        .join(Offer, Offer.product_id == Product.id, isouter=True)
        .group_by(Product.id)
        .limit(limit)
        .offset(offset)
    )

    result = await db.execute(stmt)
    rows = result.all()

    items = [
        {
            "id": row.id,
            "name": row.name,
            "thumbnail_url": row.thumbnail_object_key,
            "price": row.price_amount,
            "stock": row.stock,
            "nearest_delivery_date": row.nearest_delivery_date,
        }
        for row in rows
    ]

    return {"items": items, "limit": limit, "offset": offset}


@router.get("/{product_id}/image")
async def get_product_image_endpoint(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Serve product image from MinIO, or a transparent placeholder if no image."""
    product_stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(product_stmt)
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    key = product.image_object_key or product.thumbnail_object_key
    if not key:
        return StreamingResponse(iter([_PLACEHOLDER_GIF]), media_type="image/gif")
    try:
        stream, content_type = get_product_image(key)

        def iter_chunks():
            try:
                while True:
                    chunk = stream.read(8192)
                    if not chunk:
                        break
                    yield chunk
            finally:
                stream.close()
                stream.release_conn()

        return StreamingResponse(iter_chunks(), media_type=content_type)
    except Exception:
        return StreamingResponse(iter([_PLACEHOLDER_GIF]), media_type="image/gif")


@router.get("/{product_id}")
async def get_product_details(
    product_id: UUID,
    offers_sort: Optional[str] = Query("price", pattern="^(price|delivery_date)$"),
    db: AsyncSession = Depends(get_db),
):
    product_stmt = select(Product).where(Product.id == product_id)
    product_result = await db.execute(product_stmt)
    product = product_result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Join Seller so we return seller name and rating per offer (default sort: price)
    offers_stmt = (
        select(Offer, Seller)
        .join(Seller, Offer.seller_id == Seller.id)
        .where(Offer.product_id == product_id)
    )
    if offers_sort == "price":
        offers_stmt = offers_stmt.order_by(Offer.price_amount)
    else:
        offers_stmt = offers_stmt.order_by(Offer.delivery_date)

    offers_result = await db.execute(offers_stmt)
    rows = offers_result.all()

    attributes = [
        {"key": attr.key, "value": attr.value}
        for attr in product.product_attributes
    ]

    offers_data = [
        {
            "id": offer.id,
            "seller_id": offer.seller_id,
            "seller_name": seller.name,
            "seller_rating": float(seller.rating) if seller.rating is not None else None,
            "price_amount": offer.price_amount,
            "price_currency": offer.price_currency,
            "delivery_date": offer.delivery_date,
        }
        for offer, seller in rows
    ]

    return {
        "id": product.id,
        "name": product.name,
        "image_url": product.image_object_key,
        "attributes": attributes,
        "offers": offers_data,
    }

