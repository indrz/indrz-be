import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0', os.getenv('ALLOWED_HOSTS')]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')


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
    'rosetta',
    'corsheaders',
    'drf_yasg',

    ##### our local indrz apps
    'api',
    'buildings',
    'routing',
    'poi_manager',
    'landscape',
    'users'

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'indrz.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR,  'homepage/templates'),],
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

DATABASES = {
    'default': {
        # Postgresql with PostGIS
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'OPTIONS': {
                'options': '-c search_path=django,public'
            },
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),  # DB name
        'USER': os.getenv('POSTGRES_USER'),  # DB user name
        'PASSWORD': os.getenv('POSTGRES_PASS'),  # DB user password
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


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

LOGIN_URL = '/api/v1/admin/login/'
LOGOUT_URL = '/api/v1/admin/logout/'
LOGIN_REDIRECT_URL = '/'

STATIC_URL = os.getenv('STATIC_URL')
STATIC_FOLDER = os.getenv('STATIC_FOLDER')
STATIC_ROOT = os.getenv('STATIC_ROOT')

MEDIA_URL = os.getenv("MEDIA_URL")
MEDIA_ROOT = os.getenv('MEDIA_ROOT')


# finds all static folders in all apps
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = [
   os.path.join(BASE_DIR, STATIC_FOLDER),
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'static/admin'),
    os.path.join(BASE_DIR, 'static/legacy'),

]


UPLOAD_POI_DIR = MEDIA_ROOT + '/poi_icons/'

ROSETTA_MESSAGES_PER_PAGE = 20
YANDEX_TRANSLATE_KEY = "trnsl.1.1.20160713T103415Z.0a117baa17b2233a.fb58b4876ab2920ea22ae0a0b55507319bb4a0db"
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_WSGI_AUTO_RELOAD = False
ROSETTA_UWSGI_AUTO_RELOAD = False

# ROSETTA_STORAGE_CLASS = 'rosetta.storage.SessionRosettaStorage'


INDRZ_API_TOKEN = os.getenv('INDRZ_API_TOKEN')
IP_STARTSWITH = ""
LOCALHOST_URL = os.getenv('LOCALHOST_URL')


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_RENDERER_CLASSES': [
       'rest_framework.renderers.JSONRenderer',
       'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', )
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
}


sentry_sdk.init(
    dsn=os.getenv('SENTRY_URL'),
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000"
]


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


# if DEBUG:
#     # django-debug-toolbar
#     # ------------------------------------------------------------------------------
#
#     MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
#     INSTALLED_APPS += ('debug_toolbar',)
#     INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
#
#     DEBUG_TOOLBAR_CONFIG = {
#         'DISABLE_PANELS': [
#             'debug_toolbar.panels.redirects.RedirectsPanel',
#         ],
#         'SHOW_TEMPLATE_CONTEXT': True,
#     }

