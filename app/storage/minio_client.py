from __future__ import annotations

from functools import lru_cache
from typing import BinaryIO, Tuple

from minio import Minio

from app.core.config import get_settings


@lru_cache
def get_minio_client() -> Minio:
    settings = get_settings()
    return Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )


def ensure_bucket_exists(bucket_name: str) -> None:
    client = get_minio_client()
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)


def upload_product_image(
    file_obj: BinaryIO,
    object_name: str,
    content_type: str,
) -> str:
    settings = get_settings()
    bucket = settings.minio_bucket_products

    ensure_bucket_exists(bucket)

    client = get_minio_client()
    file_obj.seek(0, 2)
    size = file_obj.tell()
    file_obj.seek(0)

    client.put_object(
        bucket_name=bucket,
        object_name=object_name,
        data=file_obj,
        length=size,
        content_type=content_type,
    )

    return f"/products/{object_name}"


def get_product_image(object_key: str) -> Tuple[BinaryIO, str]:
    """Get image stream and content-type from MinIO. object_key is as stored in DB (e.g. /products/uuid/filename.jpg)."""
    settings = get_settings()
    bucket = settings.minio_bucket_products
    object_name = object_key.removeprefix("/products/").lstrip("/") if object_key.startswith("/") else object_key
    client = get_minio_client()
    response = client.get_object(bucket, object_name)
    content_type = response.headers.get("Content-Type", "application/octet-stream")
    return response, content_type

