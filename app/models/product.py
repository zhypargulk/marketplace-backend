from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)

    price_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    price_currency: Mapped[str] = mapped_column(String(length=3), nullable=False)

    stock: Mapped[int] = mapped_column(nullable=False, default=0)

    image_object_key: Mapped[str | None] = mapped_column(String(length=512), nullable=True)
    thumbnail_object_key: Mapped[str | None] = mapped_column(String(length=512), nullable=True)

    product_attributes: Mapped[List["ProductAttribute"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    offers: Mapped[List["Offer"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ProductAttribute(Base):
    __tablename__ = "product_attributes"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    key: Mapped[str] = mapped_column(String(length=100), nullable=False)
    value: Mapped[str] = mapped_column(String(length=255), nullable=False)

    product: Mapped[Product] = relationship(
        back_populates="product_attributes",
        lazy="selectin",
    )

