#!/bin/bash

# Add at the start
required_env_vars=("POSTGRES_DB" "POSTGRES_USER" "POSTGRES_PASS" "POSTGRES_HOST" "POSTGRES_PORT")
for var in "${required_env_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: Required environment variable '$var' is not set"
        exit 1
    fi
done

# Bash options for better error handling
set -o errexit  # Exit on error
set -o pipefail # Exit on pipe failure
set -o nounset  # Exit on undefined variable
set -o errtrace # Enable error trapping

# Trap errors and print the line number where they occur
trap 'echo "Error on line $LINENO"' ERR

# Health check function for PostgreSQL
postgres_ready() {
    python3 << END
import sys
import time
from psycopg2 import connect
from psycopg2.errors import OperationalError

start_time = time.time()
while True:
    try:
        connect(
            dbname="${POSTGRES_DB}",
            user="${POSTGRES_USER}",
            password="${POSTGRES_PASS}",
            host="${POSTGRES_HOST}",
            port="${POSTGRES_PORT}",
        )
        break
    except OperationalError:
        if time.time() - start_time > 30:  # 30 seconds timeout
            print("Database connection timeout after 30 seconds")
            sys.exit(-1)
        time.sleep(2)
END
}

# Function to run Django management commands safely
run_management_command() {
    local command="$1"
    echo "Running management command: $command"
    python3 manage.py "$command" --noinput || {
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
LOCKFILE="/app/.initialized"
if [ ! -f "$LOCKFILE" ]; then
    echo "First time setup - running initialization"

    # Run migrations first
    run_management_command "migrate"

    # Then collect static files
    run_management_command "collectstatic"

    # Create lock file with timestamp
    date > "$LOCKFILE"
    echo "Initialization complete"
fi

# Execute the main command passed to the container
echo "Starting main process..."
exec "$@"