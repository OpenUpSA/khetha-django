#!/bin/sh -ex
#
# Update requirements files from Pipfile.lock

# Include '-e .' for Herokuish.
pipenv lock --requirements >requirements.txt

# Don't include '-e .' for Tox.
pipenv lock --requirements | grep -vF '-e .' >requirements-pipenv.txt
pipenv lock --requirements --dev >requirements-pipenv-dev.txt
