from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models import Product, ProductAttribute
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate


router = APIRouter(
    prefix="/v1/admin/products",
    tags=["admin:products"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("", response_model=List[ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)) -> List[ProductOut]:
    result = await db.execute(select(Product))
    products = result.scalars().unique().all()
    return [
        ProductOut(
            id=p.id,
            name=p.name,
            price_amount=float(p.price_amount),
            price_currency=p.price_currency,
            stock=p.stock,
            image_object_key=p.image_object_key,
            thumbnail_object_key=p.thumbnail_object_key,
            attributes=[{"key": a.key, "value": a.value} for a in p.product_attributes],
            created_at=p.created_at,
            updated_at=p.updated_at,
        )
        for p in products
    ]


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
) -> ProductOut:
    product = Product(
        name=data.name,
        price_amount=data.price_amount,
        price_currency=data.price_currency,
        stock=data.stock,
        image_object_key=data.image_object_key,
        thumbnail_object_key=data.thumbnail_object_key,
    )
    db.add(product)
    await db.flush()

    for attr in data.attributes:
        db.add(ProductAttribute(product_id=product.id, key=attr.key, value=attr.value))

    await db.commit()
    await db.refresh(product)

    return ProductOut(
        id=product.id,
        name=product.name,
        price_amount=float(product.price_amount),
        price_currency=product.price_currency,
        stock=product.stock,
        image_object_key=product.image_object_key,
        thumbnail_object_key=product.thumbnail_object_key,
        attributes=[{"key": a.key, "value": a.value} for a in product.product_attributes],
        created_at=product.created_at,
        updated_at=product.updated_at,
    )


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ProductOut:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return ProductOut(
        id=product.id,
        name=product.name,
        price_amount=float(product.price_amount),
        price_currency=product.price_currency,
        stock=product.stock,
        image_object_key=product.image_object_key,
        thumbnail_object_key=product.thumbnail_object_key,
        attributes=[{"key": a.key, "value": a.value} for a in product.product_attributes],
        created_at=product.created_at,
        updated_at=product.updated_at,
    )


@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: UUID,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
) -> ProductOut:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    update_data = data.dict(exclude_unset=True)
    attributes_data = update_data.pop("attributes", None)

    for field, value in update_data.items():
        setattr(product, field, value)

    if attributes_data is not None:
        await db.execute(delete(ProductAttribute).where(ProductAttribute.product_id == product.id))
        for attr in attributes_data:
            db.add(ProductAttribute(product_id=product.id, key=attr["key"], value=attr["value"]))

    await db.commit()
    await db.refresh(product)

    return ProductOut(
        id=product.id,
        name=product.name,
        price_amount=float(product.price_amount),
        price_currency=product.price_currency,
        stock=product.stock,
        image_object_key=product.image_object_key,
        thumbnail_object_key=product.thumbnail_object_key,
        attributes=[{"key": a.key, "value": a.value} for a in product.product_attributes],
        created_at=product.created_at,
        updated_at=product.updated_at,
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    await db.delete(product)
    await db.commit()

