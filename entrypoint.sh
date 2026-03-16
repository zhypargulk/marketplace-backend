#!/bin/sh
set -e
export PYTHONPATH=/app
alembic upgrade head
exec "$@"
