import environ

env = environ.Env()


DEBUG = env("DJANGO_DEBUG", default=False)
SECRET_KEY = env("DJANGO_SECRET_KEY")

DATABASES = {"default": env.db("DJANGO_DATABASE_URL")}


ROOT_URLCONF = "khetha.urls"
