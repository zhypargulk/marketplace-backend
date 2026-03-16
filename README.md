# Marketplace Backend

FastAPI + SQLAlchemy 2 async backend for the marketplace (Vue 3 + TypeScript frontend, PostgreSQL, MinIO).

## Stack

- FastAPI
- SQLAlchemy 2.x (async, asyncpg)
- PostgreSQL
- MinIO (product images)
- Alembic (migrations)
- Pydantic settings, JWT auth

## Clone and run

### Option 1: Run with Docker Compose (recommended)

From the **marketplace-stack** directory:

```bash
cd marketplace-stack
cp .env.example .env
docker compose up --build
```

Backend: http://localhost:8000  
API docs: http://localhost:8000/docs  

Seed the database:

```bash
docker compose exec backend python seed.py
```

### Option 2: Run locally

1. Install Python 3.11+, create a venv, install deps:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Copy env and set variables (PostgreSQL and MinIO must be running):

   ```bash
   cp .env.example .env
   # Edit .env: APP_DATABASE_URL, APP_MINIO_*, APP_ADMIN_*, etc.
   ```

3. Run migrations (Alembic):

   ```bash
   alembic upgrade head
   ```

4. Start the server:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. (Optional) Seed data: `python seed.py`  
   Seed does not create product images; images are available by uploading per product in Admin (product edit or product offers page). Public image URL: `GET /v1/public/products/:id/image`.

## Tests

Smoke tests (list products, product detail 404, admin login 401):

```bash
# With venv activated and DB available
pip install -r requirements.txt
python -m pytest tests/ -v
```

Set `APP_*` env vars (or use .env) so the app can connect to a test DB.
