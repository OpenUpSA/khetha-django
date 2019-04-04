#!/bin/sh -ex
# Development helper: dump some views of the database.
cd "$(dirname "$0")"

dumpdata='django-admin dumpdata --natural-foreign --natural-primary --indent 2'

${dumpdata} --output khetha-all.json auth.group khetha
${dumpdata} --output khetha-auth.json auth.group khetha.user
${dumpdata} --output khetha-data.json --exclude khetha.user khetha
