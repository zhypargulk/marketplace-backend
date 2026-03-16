from __future__ import annotations

from typing import List
from uuid import UUID

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Seller(Base, TimestampMixin):
    __tablename__ = "sellers"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    rating: Mapped[float | None] = mapped_column(Numeric(2, 1), nullable=True)

    offers: Mapped[List["Offer"]] = relationship(
        back_populates="seller",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

