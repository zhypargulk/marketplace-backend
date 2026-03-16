# Экспорт AI-сессии (Backend) — пример 2

Второй пример экспорта для понимания процесса (§8.1).

---

## Сессия: Admin API и загрузка изображений

**Задача:** Реализовать admin CRUD продуктов (в т.ч. атрибуты), CRUD офферов, загрузку изображения продукта в MinIO.

**План:** Роутеры под префиксом /v1/admin: auth (login, JWT), products (CRUD + attributes), offers (list/create/update/delete), media (POST product image). MinIO — отдельный модуль storage/; object key сохранять в product.image_object_key и thumbnail_object_key.

**Генерация (AI):** Роутеры в app/api/routers/admin/; get_current_admin dependency; media.py с multipart/form-data и вызовом upload_product_image; ProductUpdate с поддержкой attributes.

**Проверка:** Ручные запросы: логин → токен → создание продукта → обновление атрибутов → создание оффера → загрузка файла → проверка GET image.

**Исправление:** Приведение схем к единому формату (attributes как list of {key, value}); проверка существования product/seller при создании оффера.

**Итог:** Admin API и загрузка изображений работают; контракты зафиксированы в schemas и проверяются вручную.
