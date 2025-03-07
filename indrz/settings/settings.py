from logging import config
import os
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DEBUG'))

if not DEBUG:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(' ')
    CSRF_ALLOWED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(' ')
    # # Ensure CSRF_COOKIE settings are correctly set
    CSRF_COOKIE_SECURE = bool(os.getenv('CSRF_COOKIE_SECURE'))  # Set to True in production
    SESSION_COOKIE_SECURE = bool(os.getenv('SESSION_COOKIE_SECURE'))  # Set to True in production with HTTPS

    sentry_sdk.init(
        dsn=os.getenv('SENTRY_URL'),
        integrations=[DjangoIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.5,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

if os.name == 'nt':
    import platform
    OSGEO4W = r"C:\OSGeo4W"
    if '64' in platform.architecture()[0]:
        OSGEO4W += "64"
    assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r"\share\epsg_csv"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"


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
    'corsheaders',
    'drf_yasg',

    ##### our local indrz apps
    'organizations.apps.OrganizationsConfig',
    'api',
    'buildings',
    'routing',
    'poi_manager',
    'landscape',
    'users'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]


# CORS_ORIGIN_WHITELIST = os.getenv('CORS_ORIGIN_WHITELIST').split(' ')
# CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split(' ')



ROOT_URLCONF = 'indrz.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
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
                'django.template.context_processors.request',
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
                'options': '-c search_path=django,geodata,public'
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
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, STATIC_FOLDER),
#     os.path.join(BASE_DIR, 'static'),
#     os.path.join(BASE_DIR, 'static/admin'),
#     os.path.join(BASE_DIR, 'static/legacy'),
#
# ]


UPLOAD_POI_DIR = MEDIA_ROOT + '/poi_icons/'


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



LOGFILE_DIR = os.getenv('LOGFILE_DIR')
# Set the maximum log file size (50 MB in bytes)
LOG_MAX_SIZE = 50 * 1024 * 1024  # 50 MB

