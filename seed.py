from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta
from random import randint

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.models import Offer, Product, ProductAttribute, Seller


fake = Faker()


async def seed_database() -> None:
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        await _seed(session)


async def _seed(session: AsyncSession) -> None:
    sellers = [
        Seller(id=uuid.uuid4(), name=fake.company(), rating=round(fake.pyfloat(min_value=1, max_value=5), 1))
        for _ in range(10)
    ]
    session.add_all(sellers)
    await session.flush()

    products: list[Product] = []
    for _ in range(100):
        product = Product(
            id=uuid.uuid4(),
            name=fake.word().title(),
            price_amount=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            price_currency="USD",
            stock=randint(0, 100),
        )
        session.add(product)
        products.append(product)

    await session.flush()

    now = datetime.utcnow()
    for product in products:
        # attributes 2–6
        for _ in range(randint(2, 6)):
            attr = ProductAttribute(
                id=uuid.uuid4(),
                product_id=product.id,
                key=fake.word(),
                value=fake.word(),
            )
            session.add(attr)

        # offers 2–10
        for _ in range(randint(2, 10)):
            seller = sellers[randint(0, len(sellers) - 1)]
            delivery_date = now.date() + timedelta(days=randint(0, 6))
            offer = Offer(
                id=uuid.uuid4(),
                product_id=product.id,
                seller_id=seller.id,
                price_amount=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
                price_currency="USD",
                delivery_date=delivery_date,
            )
            session.add(offer)

    await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_database())

