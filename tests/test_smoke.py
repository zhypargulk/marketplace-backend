"""Smoke tests: list products, product detail, admin login (spec §2.2, §5.5)."""
from __future__ import annotations

import uuid

import pytest


def test_public_list_products(client):
    """GET /v1/public/products returns 200 and items array."""
    response = client.get("/v1/public/products", params={"limit": 5})
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "limit" in data
    assert isinstance(data["items"], list)


def test_public_product_detail_not_found(client):
    """GET /v1/public/products/:id returns 404 for unknown id."""
    fake_id = uuid.uuid4()
    response = client.get(f"/v1/public/products/{fake_id}")
    assert response.status_code == 404


def test_admin_login_invalid_credentials(client):
    """POST /v1/admin/auth/login returns 401 for wrong credentials."""
    response = client.post(
        "/v1/admin/auth/login",
        json={"email": "wrong@example.com", "password": "wrong"},
    )
    assert response.status_code == 401
