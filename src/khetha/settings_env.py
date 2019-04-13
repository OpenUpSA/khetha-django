from datetime import timedelta

import environ

env = environ.Env()


# Environment-based Django settings:

DEBUG = env("DJANGO_DEBUG", default=False)
SECRET_KEY = env("DJANGO_SECRET_KEY")

if "DJANGO_DATABASE_URL" in env:  # pragma: no cover
    DATABASES = {"default": env.db("DJANGO_DATABASE_URL")}
if "DJANGO_STATIC_URL" in env:  # pragma: no cover
    STATIC_URL = env("DJANGO_STATIC_URL")
if "DJANGO_STATIC_ROOT" in env:  # pragma: no cover
    STATIC_ROOT = env.path("DJANGO_STATIC_ROOT")()
if "DJANGO_ALLOWED_HOSTS" in env:  # pragma: no cover
    ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

if "DJANGO_STATICFILES_DIRS" in env:  # pragma: no cover
    # XXX (Pi): Move this into django-environ-base.
    #
    # This:
    #
    #   DJANGO_STATICFILES_DIRS=node_modules,assets:build/assets
    #
    # Will yield this:
    #
    #   STATICFILES_DIRS = [
    #       'node_modules',
    #       ("assets", "build/assets"),
    #   ]
    #
    STATICFILES_DIRS = env.list(
        "DJANGO_STATICFILES_DIRS",
        cast=lambda s: (tuple(s.split(":")) if ":" in s else s),
    )
# XXX: Skip this if empty, to avoid inadvertently changing
# the default StaticFilesStorage to DEFAULT_FILE_STORAGE.
if env("DJANGO_STATICFILES_STORAGE", default=""):  # pragma: no cover
    STATICFILES_STORAGE = env("DJANGO_STATICFILES_STORAGE")

if "WHITENOISE_KEEP_ONLY_HASHED_FILES" in env:  # pragma: no cover
    WHITENOISE_KEEP_ONLY_HASHED_FILES = env.bool("WHITENOISE_KEEP_ONLY_HASHED_FILES")

GOOGLE_MAPS_API_KEY: str
if "GOOGLE_MAPS_API_KEY" in env:  # pragma: no cover
    GOOGLE_MAPS_API_KEY = env("GOOGLE_MAPS_API_KEY")

# django-analytical

if "GOOGLE_ANALYTICS_PROPERTY_ID" in env:  # pragma: no cover
    GOOGLE_ANALYTICS_PROPERTY_ID = env("GOOGLE_ANALYTICS_PROPERTY_ID")


# Other Django settings:

ROOT_URLCONF = "khetha.urls"

INSTALLED_APPS = [
    # Khetha
    "khetha",
    # Third-party libraries
    "adminsortable2",
    "analytical",
    # Django defaults
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
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
