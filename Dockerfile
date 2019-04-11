# Dockerfile for a base deployable khetha-django instance.

# Base Python image
FROM python:3.7-alpine AS base-python
ENV PATH="/root/.local/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1

# Collect NPM assets.
FROM node:alpine AS npm-assets-builder
WORKDIR /khetha-django
COPY package.json .
COPY package-lock.json .
COPY build-assets.sh .
RUN npm install
RUN ./build-assets.sh
# Output: /khetha-django/build/assets/

# Build Khetha Python wheels
# https://github.com/PiDelport/docker-python-c-package-builder
FROM pidelport/python-c-package-builder:latest AS khetha-wheels-builder
WORKDIR /khetha-django
# First build khetha-django's requirements-pipenv.txt separately, for better caching.
COPY requirements-pipenv.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir=/wheels -r requirements-pipenv.txt
# Build khetha-django itself.
COPY .git .git
COPY README.md .
COPY setup.cfg .
COPY setup.py .
COPY src src
RUN pip wheel --no-cache-dir --no-deps --wheel-dir=/wheels .
# Output: /wheels/

# Build the installed Khetha site and static files
FROM base-python AS khetha-site-builder
COPY --from=npm-assets-builder /khetha-django/build/assets/ /khetha-django/build/assets/
COPY --from=khetha-wheels-builder /wheels/ /wheels/
RUN pip install --no-cache-dir --no-deps --no-index --user /wheels/*.whl

# Tell collectstatic where to find the static assets collected by build-assets.sh
ENV DJANGO_STATICFILES_DIRS='assets:/khetha-django/build/assets'

# Shared block: Base Django settings
ENV DJANGO_SETTINGS_MODULE=khetha.settings_env
ENV DJANGO_STATIC_URL='/static/'
ENV DJANGO_STATIC_ROOT='/static_root/'
# Build args
ARG DJANGO_STATICFILES_STORAGE
ENV DJANGO_STATICFILES_STORAGE="${DJANGO_STATICFILES_STORAGE}"
ARG WHITENOISE_KEEP_ONLY_HASHED_FILES
ENV WHITENOISE_KEEP_ONLY_HASHED_FILES="${WHITENOISE_KEEP_ONLY_HASHED_FILES}"

ENV DJANGO_SECRET_KEY=dummy-secret-key-for-collectstatic
# --verbosity 2 lists the collected files, for build logs.
RUN django-admin collectstatic --verbosity 2
# Output: /root/.local/
# Output: /static_root/

# Final Django image.
FROM base-python AS khetha-django
# psycopg2 runtime dependency:
RUN apk add --no-cache libpq
COPY --from=khetha-site-builder /root/.local /root/.local
# XXX: Include the static files in this image, for now.
# (This should be better done as a separate build output stage,
# but support for this is still immature in the Docker ecosystem.)
COPY --from=khetha-site-builder /static_root /static_root

# Shared block: Base Django settings
ENV DJANGO_SETTINGS_MODULE=khetha.settings_env
ENV DJANGO_STATIC_URL='/static/'
ENV DJANGO_STATIC_ROOT='/static_root/'
# Build args
ARG DJANGO_STATICFILES_STORAGE
ENV DJANGO_STATICFILES_STORAGE="${DJANGO_STATICFILES_STORAGE}"
ARG WHITENOISE_KEEP_ONLY_HASHED_FILES
ENV WHITENOISE_KEEP_ONLY_HASHED_FILES="${WHITENOISE_KEEP_ONLY_HASHED_FILES}"
