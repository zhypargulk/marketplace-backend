# Экспорт AI-сессии (Backend) — пример 1

Файл для соответствия §8.1. Реальные экспорты сохранять как `session-YYYY-MM-DD.md` или `*.jsonl`.

---

## Сессия: публичный API и smoke-тесты

**Задача:** В деталях продукта возвращать seller_name и seller_rating для офферов; сортировка по умолчанию — по цене; добавить smoke-тесты.

**План:** Изменить GET /v1/public/products/{id}: join с Seller, добавить поля в ответ; default offers_sort=price. Написать тесты: list (200), detail 404, login 401.

**Генерация (AI):** Правки в catalog.py (select Offer+Seller, order_by, offers_data с seller_name/seller_rating); добавление tests/test_smoke.py и tests/conftest.py; pytest, httpx в requirements.txt.

**Проверка:** Ручные запросы к API; `pytest tests/ -v` при поднятой БД.

**Исправление:** Уточнение импортов (status, HTTPException), порядок полей в ответе.

**Итог:** Контракт и тесты соответствуют требованиям; процесс управляемый (план → генерация → проверка → исправление).
