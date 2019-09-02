
"""
WSGI config for indrz project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import site

from django.core.wsgi import get_wsgi_application


# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/wsgi/.local/lib/python3.6/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/srv/www/campusplan.aau.at/wsgi/indrz')
sys.path.append('/srv/www/campusplan.aau.at/wsgi/indrz/indrz')

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production_settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.settings'

application = get_wsgi_application()
