from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin
from .product import Product
from .seller import Seller


class Offer(Base, TimestampMixin):
    __tablename__ = "offers"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    seller_id: Mapped[UUID] = mapped_column(
        ForeignKey("sellers.id", ondelete="CASCADE"),
        nullable=False,
    )

    price_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    price_currency: Mapped[str] = mapped_column(String(length=3), nullable=False)

    delivery_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    product: Mapped[Product] = relationship(
        back_populates="offers",
        lazy="selectin",
    )
    seller: Mapped[Seller] = relationship(
        back_populates="offers",
        lazy="selectin",
    )

