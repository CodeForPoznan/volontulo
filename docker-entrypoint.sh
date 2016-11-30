#!/bin/bash
set -e

sleep 5  # waits for another container to be ready

python3 manage.py migrate --settings=volontulo_org.settings.docker
python3 manage.py loaddata initial/data.json --settings=volontulo_org.settings.docker
python3 manage.py runserver --settings=volontulo_org.settings.docker 0.0.0.0:8000
