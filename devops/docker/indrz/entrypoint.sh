#!/bin/bash

set -xe

if [[ "$RUN_MIGRATIONS" == "1" ]]; then
    # Execute migrations
    $APP_ROOT/manage.py migrate --noinput
    # Collect static
    $APP_ROOT/manage.py collectstatic --noinput
fi

# Execute subcommand, wrapping
exec "$@"
