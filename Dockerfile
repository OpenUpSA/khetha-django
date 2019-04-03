# Dockerfile for a base deployable khetha-django instance.

# Base Python image
FROM python:3.7-alpine AS base-python
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
WORKDIR /khetha-django
COPY --from=npm-assets-builder /khetha-django/build/assets/ /khetha-django/build/assets/
COPY --from=khetha-wheels-builder /wheels/ /wheels/
ENV PATH="/root/.local/bin:${PATH}"
RUN pip install --no-cache-dir --no-deps --no-index --user /wheels/*.whl
# Build the static files.
# NOTE: This won't get used unless you extract it from this stage as part of your deployment.
ENV DJANGO_SETTINGS_MODULE=khetha.settings_env
ENV DJANGO_SECRET_KEY=dummy-secret-key-for-collectstatic
ENV DJANGO_STATIC_URL='/static/'
ENV DJANGO_STATIC_ROOT='/static_root/'
RUN django-admin collectstatic
# Output: /root/.local/
# Output: /static_root/

# Final Django image.
FROM base-python AS khetha-django
# psycopg2 runtime dependency:
RUN apk add --no-cache libpq
COPY --from=khetha-site-builder /root/.local /root/.local
ENV PATH="/root/.local/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=khetha.settings_env
ENV DJANGO_STATIC_URL='/static/'
