from django.http import JsonResponse, HttpResponse
from django.views import View
from indrz import __version__
from django.db import connections
from django.db.utils import OperationalError
import datetime

def version_view(request):
    """Return the project version as plain text."""
    return HttpResponse(__version__)

class VersionAPIView(View):
    """Return the project version as JSON."""
    def get(self, request):
        return JsonResponse({
            "project": "indrz",
            "version": __version__
        })

def health_check(request):
    # Check database connection
    db_healthy = True
    try:
        connections['default'].ensure_connection()
    except OperationalError:
        db_healthy = False

    # Get version from environment variable or settings
    version = __version__

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
