#!/bin/bash
set -e

wait-for-it db:5432

python3 manage.py migrate --settings=volontulo_org.settings.docker
python3 manage.py loaddata initial/data.json --settings=volontulo_org.settings.docker
python3 manage.py runserver --settings=volontulo_org.settings.docker 0.0.0.0:8000
