from datetime import timedelta

import environ, os

env = environ.Env()


# Environment-based Django settings:

DEBUG = os.environ.get('DJANGO_DEBUG', 'true') == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = 'not-secret-for-dev'
else:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

import dj_database_url
DATABASE_URL = env('DJANGO_DATABASE_URL', default='postgres://postgres@localhost:5432/postgres')
db_config = dj_database_url.parse(DATABASE_URL)
db_config['ATOMIC_REQUESTS'] = True
DATABASES = {
    'default': db_config,
}

ALLOWED_HOSTS = ['*']

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


######===========================
# Static files
#--------------------------

ASSETS_DEBUG = DEBUG
ASSETS_URL_EXPIRE = False

# where the compiled assets go
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# the URL for assets
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    'node_modules',
]
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

#-------------
# End static files stuff
######======================



if "GOOGLE_MAPS_API_KEY" in env:  # pragma: no cover
    GOOGLE_MAPS_API_KEY = env("GOOGLE_MAPS_API_KEY")


# Other Django settings:

ROOT_URLCONF = "khetha.urls"

INSTALLED_APPS = [
    # Khetha
    "khetha",
    # Third-party libraries
    "adminsortable2",
    # Django defaults
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    # Django default:
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise: After SecurityMiddleware, before everything else.
    # http://whitenoise.evans.io/en/stable/django.html#enable-whitenoise
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Django defaults:
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

AUTH_USER_MODEL = "khetha.User"


# Time zone (hard-coded, for now)
USE_TZ = True
TIME_ZONE = "Africa/Johannesburg"


# Khetha relies on session persistence to identify people:
# increase the default 2 week lifetime to something long.
SESSION_COOKIE_AGE = timedelta(days=1000).total_seconds()

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR'
    },
    'loggers': {
        # put any custom loggers here
        # 'your_package_name': {
        #    'level': 'DEBUG' if DEBUG else 'INFO',
        # },
        'django': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        }
    }
}
