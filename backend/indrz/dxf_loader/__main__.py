import os
import argparse
# from django.core.wsgi import get_wsgi_application

# Set the DJANGO_SETTINGS_MODULE environment variable
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

# Initialize Django
# application = get_wsgi_application()

from .monitor import run_cycle

parser = argparse.ArgumentParser(description="DXF nightly importer")
parser.add_argument("--once", action="store_true", help="run one cycle immediately")
args = parser.parse_args()

if __name__ == "__main__" and not args.once:
    # Run the monitoring cycle indefinitely
    while True:
        if args.once:
            run_cycle()