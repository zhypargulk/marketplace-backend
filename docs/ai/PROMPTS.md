# PROMPTS.md — наиболее важные промпты и правила (Backend)

Опциональный, но приветствуемый артефакт §8.1. Примеры промптов и правила для последующих итераций.

---

## 1. Архитектура и контракты

- «Спроектируй production-ready FastAPI backend для маркетплейса: async SQLAlchemy 2.x, asyncpg, Alembic, PostgreSQL, MinIO. Публичный каталог (список товаров, детали с офферами и продавцом), admin CRUD и JWT. Дай структуру папок и модулей, без кода.»
- «Контракт: GET /v1/public/products/{id} возвращает offers с полями seller_id, seller_name, seller_rating; параметр offers_sort (price | delivery_date), по умолчанию price.»

---

## 2. Модели и API

- «Добавь в ответ деталей продукта seller_name и seller_rating для каждого оффера; join с таблицей sellers. Сортировка офферов по умолчанию — по цене.»
- «Реализуй POST /v1/admin/products/{id}/image: multipart/form-data, загрузка в MinIO, сохранение object key в product.image_object_key и thumbnail_object_key.»
- «Добавь smoke-тесты: GET /v1/public/products (200, items), GET product с несуществующим UUID (404), POST /v1/admin/auth/login с неверным паролем (401).»

---

## 3. Инфраструктура

- «В .env.example перечисли все APP_* переменные: DB URL, JWT secret, admin email/password, MinIO endpoint/access/secret/bucket. Без реальных секретов.»

---

## 4. Правила для последующих итераций (копировать в промпты)

- Все роуты, обращающиеся к БД, — async; использовать AsyncSession из get_db.
- Новые поля в ответах API отражать в Pydantic-схемах и при необходимости в миграциях Alembic.
- Секреты и пароли — только в переменных окружения; в репозитории только .env.example с placeholder-значениями.
- MinIO и работа с файлами — изолированы в storage/; в роутерах только вызов функций и запись object key в модель.
- После изменения контракта API — обновить smoke-тесты и при необходимости описание в README.
