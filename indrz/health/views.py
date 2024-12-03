# health/views.py
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
import datetime
import os

def health_check(request):
    # Check database connection
    db_healthy = True
    try:
        connections['default'].ensure_connection()
    except OperationalError:
        db_healthy = False

    # Get version from environment variable or settings
    version = os.getenv('APP_VERSION', '1.0.0')  # You can set this in your Dockerfile or settings

    health_status = {
        'status': 'healthy' if db_healthy else 'unhealthy',
        'version': version,
        'timestamp': datetime.datetime.now().isoformat(),
        'database': {
            'status': 'connected' if db_healthy else 'disconnected',
        }
    }

    status_code = 200 if db_healthy else 503
    return JsonResponse(health_status, status=status_code)



