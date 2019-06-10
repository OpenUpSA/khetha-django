khetha-django
=============

[Jump to Production Deployment](#production-deployment)

Development Quickstart
----------


```shell
npm install
```

Start PostgreSQL and the app:

```
docker-compose up
```

Set up database tables first time you set up the database

```
docker-compose run --rm web django-admin migrate
docker-compose run --rm web django-admin createsuperuser
```

Load some development data

```
docker-compose run --rm web django-admin loaddata sample-task-data.json
```

To attach a `psql` shell:

    docker-compose exec --user postgres db psql

### Run the tests:

Ensure postgres is running with the required user and DB, e.g. using docker-compose:

```
docker-compose up db
```

If using docker-compose as above, then run the tests in another shell:

```
tox
```

### Create an environment and run a development server:

```
django-admin check
django-admin runserver
```

Working with data
-----------------

To dump the task data, or update [src/khetha/fixtures/sample-task-data.json]:

```shell
django-admin dumpdata --indent 2 khetha.task khetha.question khetha.answeroption

meld <(django-admin dumpdata --indent 2 khetha.task khetha.question khetha.answeroption) src/khetha/fixtures/sample-task-data.json
```

[src/khetha/fixtures/sample-task-data.json]: src/khetha/fixtures/sample-task-data.json

Production Deployment
---------------------

```
dokku app:create khetha
dokku domains:add khetha khetha.org.za
dokku config:set khetha DJANGO_DEBUG=False \
                        DISABLE_COLLECTSTATIC=1 \
                        DJANGO_SECRET_KEY=... \
                        DJANGO_DATABASE_URL=... \
                        GOOGLE_MAPS_API_KEY=... \
                        DISABLE_COLLECTSTATIC=1 \
                        GOOGLE_ANALYTICS_PROPERTY_ID=UA-93649482-14 \
                        SENTRY_DSN=https://... \
                        DJANGO_SECRET_KEY=...
```