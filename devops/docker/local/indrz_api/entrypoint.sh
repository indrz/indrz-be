#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o errtrace

trap 'echo "Error on line ${LINENO}" >&2' ERR

required_env_vars=("POSTGRES_DB" "POSTGRES_USER" "POSTGRES_PASS" "POSTGRES_HOST" "POSTGRES_PORT")
for var in "${required_env_vars[@]}"; do
    if [ -z "${!var:-}" ]; then
        echo "Error: Required environment variable '$var' is not set" >&2
        exit 1
    fi
done

APP_DIR="${APP_DIR:-/app}"
LOCKFILE="${APP_DIR}/.initialized"

if [ ! -f "${APP_DIR}/manage.py" ]; then
    echo "Error: ${APP_DIR}/manage.py not found. Check docker-compose bind mount for ${APP_DIR}." >&2
    echo "Hint: local setup expects ./backend/indrz to be mounted at ${APP_DIR}." >&2
    exit 1
fi

cd "${APP_DIR}"

# Health check function for PostgreSQL
postgres_ready() {
    python3 << END
import sys
import time
from psycopg2 import connect, OperationalError

timeout_seconds = int("${POSTGRES_CONNECT_TIMEOUT:-30}")
start_time = time.time()
while True:
    try:
        conn = connect(
            dbname="${POSTGRES_DB}",
            user="${POSTGRES_USER}",
            password="${POSTGRES_PASS}",
            host="${POSTGRES_HOST}",
            port="${POSTGRES_PORT}",
            connect_timeout=5,
        )
        conn.close()
        break
    except OperationalError:
        if time.time() - start_time > timeout_seconds:
            print(f"Database connection timeout after {timeout_seconds} seconds")
            sys.exit(-1)
        time.sleep(2)
END
}

# Function to run Django management commands safely
run_management_command() {
    local command="$1"
    shift || true
    echo "Running management command: $command"
    python3 manage.py "$command" "$@" || {
        echo "Failed to run $command"
        exit 1
    }
}

# Wait for database
echo "Waiting for PostgreSQL to become available..."
if ! postgres_ready; then
    echo "Could not connect to PostgreSQL"
    exit 1
fi
echo "PostgreSQL is available"

# Initialize database if needed
if [ ! -f "$LOCKFILE" ]; then
    echo "First time setup - running initialization"

    # Run migrations first
    run_management_command "migrate" --noinput

    # Then collect static files
    run_management_command "collectstatic" --noinput

    run_management_command "create_superuser"
    
    # Create lock file with timestamp
    date > "$LOCKFILE"
    echo "Initialization complete"
fi

# Execute the main command passed to the container
echo "Starting main process..."
exec "$@"
