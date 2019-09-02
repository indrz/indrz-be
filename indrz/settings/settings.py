import os
import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('secret_key')
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'campusplan.aau.at', 'campus-gis.aau.at', ]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')
COMPRESS_ENABLED = os.getenv('COMPRESSED_ENABLED')

AUTH_USER_MODEL = 'users.User'  # my app is called users  hence users.User I could make app called core.Users

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    #### third party apps
    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',
    'taggit',
    'mptt',
    'rest_framework_swagger',
    'rosetta',
    'compressor',
    'raven.contrib.django.raven_compat',


    ##### our local indrz apps
    'api',
    # 'maps',
    'buildings',
    'routing',
    # 'conference',
    'poi_manager',
    'landscape',
    'homepage',
    'bookway',
    'kiosk',
    'users'

]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]


ROOT_URLCONF = 'indrz.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,  'templates'),
                 # os.path.join(BASE_DIR,  'maps/templates'),
                 os.path.join(BASE_DIR,  'poi_manager/templates'),
                 os.path.join(BASE_DIR,  'homepage/templates'),
                 os.path.join(BASE_DIR, 'bookway/templates'),
                 os.path.join(BASE_DIR,  'kiosk/templates'),
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            # not needed if APP_DIRS is true
            # 'loaders':[(
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader',)]
        },
    },
]


WSGI_APPLICATION = 'indrz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        # Postgresql with PostGIS
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('db_name'),  # DB name
        'USER': os.getenv('db_user'),  # DB user name
        'PASSWORD': os.getenv('db_pwd'),  # DB user password
        'HOST': os.getenv('db_host'),

        # 'NAME': secret_settings.db_prod_name, # DB name
        # 'USER': secret_settings.db_prod_user, # DB user name
        # 'PASSWORD': secret_settings.db_prod_pwd, # DB user password
        # 'HOST': secret_settings.db_prod_host,
        'PORT': os.getenv('db_port'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', 'English'),
    ('de', 'Deutsch'))

# Location of translation files
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

TIME_ZONE = 'Europe/Vienna'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_FOLDER = 'static'
STATIC_ROOT = os.getenv('STATIC_ROOT')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.getenv('MEDIA_ROOT')

STATICFILES_DIRS = [
   os.path.join(BASE_DIR, STATIC_FOLDER),

]

STATICFILES_DIRS += [
    os.path.join(BASE_DIR, 'homepage/static'),
    os.path.join(BASE_DIR, 'static/admin'),
    os.path.join(BASE_DIR, 'static/gis')

]

# finds all static folders in all apps
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'compressor.finders.CompressorFinder',
)


UPLOAD_POI_DIR = MEDIA_ROOT + '/poi-icons/'

ROSETTA_MESSAGES_PER_PAGE = 20
YANDEX_TRANSLATE_KEY = "trnsl.1.1.20160713T103415Z.0a117baa17b2233a.fb58b4876ab2920ea22ae0a0b55507319bb4a0db"
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_WSGI_AUTO_RELOAD = False
ROSETTA_UWSGI_AUTO_RELOAD = False

# ROSETTA_STORAGE_CLASS = 'rosetta.storage.SessionRosettaStorage'


INDRZ_API_TOKEN = os.getenv('INDRZ_API_TOKEN')
IP_STARTSWITH = "137.208."
LOCALHOST_URL = os.getenv('LOCALHOST_URL') #'"https://campusplan.aau.at/"  # http://campus.wu.ac.at


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_RENDERER_CLASSES': [
       'rest_framework.renderers.JSONRenderer',
       'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', )
}

RAVEN_URL = os.getenv('RAVEN_URL')
sentry_sdk.init(RAVEN_URL, integrations=[DjangoIntegration()])

# RAVEN_CONFIG = {'dsn': RAVEN_URL,
#     # 'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
# }


if os.path.isdir(os.getenv('LOGFILE_DIR')):
    LOGGING_CONFIG = None

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'file_verbose': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': '/srv/indrz_logs/verbose.log',
                'formatter': 'verbose'
            },
            'file_debug': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': '/srv/indrz_logs/debug.log',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers':['file_verbose'],
                'propagate': True,
                'level':'DEBUG',
            },
            'api': {
                'handlers': ['file_debug'],
                'propagate': True,
                'level': 'DEBUG',
            },
            'admin': {
                'handlers': ['file_debug'],
                'propagate': True,
                'level': 'DEBUG',
            },
            'buildings': {
                'handlers': ['file_debug'],
                'propagate': True,
                'level': 'DEBUG',
            },
            'routing': {
                'handlers': ['file_debug'],
                'propagate': True,
                'level': 'DEBUG',
            },
            'maps': {
                'handlers': ['file_debug'],
                'propagate': True,
                'level': 'DEBUG',
            }

        }
    }

    import logging.config
    logging.config.dictConfig(LOGGING)


if DEBUG:
    # django-debug-toolbar
    # ------------------------------------------------------------------------------

    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]

    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
    }

