import os
import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY')
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

    ##### our local indrz apps
    'api',
    'buildings',
    'routing',
    'poi_manager',
    'landscape',
    'homepage',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'poi_manager/templates'),
                 os.path.join(BASE_DIR, 'homepage/templates'),
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
        'NAME': os.getenv('DB_NAME'),  # DB name
        'USER': os.getenv('DB_USER'),  # DB user name
        'PASSWORD': os.getenv('DB_PASS'),  # DB user password
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
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


STATIC_URL = os.getenv('STATIC_URL')
STATIC_FOLDER = os.getenv('STATIC_FOLDER')
STATIC_ROOT = os.getenv('STATIC_ROOT')

MEDIA_URL = os.getenv("MEDIA_URL")
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


sentry_sdk.init(os.getenv('SENTRY_URL'), integrations=[DjangoIntegration()])

LOGFILE_DIR = os.getenv('LOGFILE_DIR')

if os.path.isdir(LOGFILE_DIR):
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
                'filename': os.path.join(LOGFILE_DIR, 'verbose.log'),
                'formatter': 'verbose'
            },
            'file_debug': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(LOGFILE_DIR, 'debug.log'),
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

