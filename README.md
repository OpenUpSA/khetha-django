khetha-django
=============

Quickstart
----------

Start PostgreSQL:

```
docker-compose up
```

Run the tests:

```
tox
```

Create an environment and run a development server:

```
cp -p .env.example .env

pipenv shell
pipenv install --dev

django-admin check
django-admin runserver
```

(Or use PyCharm.)


Updating dependencies
---------------------

Use Pipenv, and run [requirements-update.sh] after any Pipfile.lock update.
