#!/bin/bash

# entrypoint.sh file of Dockerfile

# Section 1- Bash options
set -o errexit
set -o pipefail
set -o nounset

# Section 2: Health of dependent services
postgres_ready() {
    python3 << END
import sys

from psycopg2 import connect
from psycopg2.errors import OperationalError

try:
    connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASS}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
except OperationalError:
    sys.exit(-1)
END
}


until postgres_ready; do
  >&2 echo "Waiting for PostgreSQL to become available..."
  sleep 5
done
>&2 echo "PostgreSQL is available"


# Section 3- Idempotent Django commands
# python3 manage.py collectstatic --noinput
# python3 manage.py makemigrations
# python3 manage.py migrate


exec "$@"