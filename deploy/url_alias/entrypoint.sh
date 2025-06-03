#!/bin/bash
set -e

echo "🔄 Startup migrations..."
alembic upgrade head

echo "🚀 Startup API server..."
python -m url_alias
