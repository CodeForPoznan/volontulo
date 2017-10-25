#!/bin/bash
set -e

# we need to re-create static directory during creation of container because
# mounted volume overwrites all files available during build phase:
if [ ! -f apps/volontulo/static ]; then
    cd apps/volontulo;
    node node_modules/.bin/gulp build;
    cd -;
fi

wait-for-it db:5432

python3 manage.py migrate
python3 manage.py loaddata initial/data.json
python3 manage.py runserver 0.0.0.0:8000