"""Pytest fixtures for marketplace backend tests."""
from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

# Ensure test env has required vars so Settings can load (e.g. in CI)
os.environ.setdefault("APP_DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/marketplace_test")
os.environ.setdefault("APP_JWT_SECRET_KEY", "test-secret-key-change-in-production")
os.environ.setdefault("APP_ADMIN_EMAIL", "admin@test.example")
os.environ.setdefault("APP_ADMIN_PASSWORD", "admin")
os.environ.setdefault("APP_MINIO_ENDPOINT", "localhost:9000")
os.environ.setdefault("APP_MINIO_ACCESS_KEY", "minioadmin")
os.environ.setdefault("APP_MINIO_SECRET_KEY", "minioadmin")

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
