from __future__ import annotations

import uuid
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models import Product
from app.storage.minio_client import upload_product_image


router = APIRouter(
    prefix="/v1/admin/products",
    tags=["admin:media"],
    dependencies=[Depends(get_current_admin)],
)


@router.post("/{product_id}/image")
async def upload_product_image_endpoint(
    product_id: UUID,
    file: Annotated[UploadFile, File(...)] ,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    ext = (file.filename or "").rsplit(".", 1)[-1].lower() if file.filename else "bin"
    object_name = f"{product_id}/{uuid.uuid4()}.{ext}"

    image_path = upload_product_image(file.file, object_name, file.content_type or "application/octet-stream")

    product.image_object_key = image_path
    product.thumbnail_object_key = image_path  # реальный thumbnail можно добавить позже

    await db.commit()
    await db.refresh(product)

    return {
        "image_url": image_path,
        "thumbnail_url": image_path,
    }

