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
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    # Django defaults
    "django.middleware.security.SecurityMiddleware",
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


# Tell collectstatic where to find the static assets collected by build-assets.sh
# (XXX: This should go in dev/build config.)
STATICFILES_DIRS = [("assets", "build/assets")]
