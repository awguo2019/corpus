#!/bin/sh
set -e

cd /app

# Show where we are and that alembic.ini exists
echo "[entrypoint] CWD=$(pwd)"
if [ ! -f alembic.ini ]; then
  echo "[entrypoint] ERROR: alembic.ini not found in $(pwd)" >&2
  ls -la
  exit 1
fi

# Wait for DB if needed
if [ -n "$DATABASE_URL" ]; then
  echo "[entrypoint] DATABASE_URL detected"
fi

# Run migrations
echo "[entrypoint] Running alembic upgrade head..."
alembic upgrade head || {
  echo "[entrypoint] Alembic failed; printing config and tree" >&2
  grep -n "^\[alembic\]" -n alembic.ini || true
  ls -la /app
  exit 1
}

# Start the app (pass through CMD/compose command)
echo "[entrypoint] Starting app: $@"
exec "$@"
