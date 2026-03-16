from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.public import catalog
from app.api.routers.admin import auth as admin_auth
from app.api.routers.admin import products as admin_products
from app.api.routers.admin import sellers as admin_sellers
from app.api.routers.admin import offers as admin_offers
from app.api.routers.admin import media as admin_media


def create_app() -> FastAPI:
    app = FastAPI(title="Marketplace Backend")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:80", "http://127.0.0.1:80"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Public
    app.include_router(catalog.router)

    # Admin
    app.include_router(admin_auth.router)
    app.include_router(admin_products.router)
    app.include_router(admin_sellers.router)
    app.include_router(admin_offers.router)
    app.include_router(admin_media.router)

    return app


app = create_app()
