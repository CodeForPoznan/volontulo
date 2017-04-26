#!/bin/bash
set -e

# we need to re-create local_config.yaml during creation of container because
# mounted volume overwrites all files available during build phase:
if [ ! -f local_config.yaml ]; then
    cp etc/local_config.yaml.sample local_config.yaml;
    sed '/^secret_key/ d' local_config.yaml > tmp.yaml && mv tmp.yaml local_config.yaml;
    echo "secret_key: $SECRET_KEY" >> local_config.yaml;
fi

# we need to re-create static directory during creation of container because
# mounted volume overwrites all files available during build phase:
if [ ! -f apps/volontulo/static ]; then
    cd apps/volontulo;
    node node_modules/.bin/gulp build;
    cd -;
fi

wait-for-it db:5432

python3 manage.py migrate --settings=volontulo_org.settings.dev_docker
python3 manage.py loaddata initial/data.json --settings=volontulo_org.settings.dev_docker
python3 manage.py runserver --settings=volontulo_org.settings.dev_docker 0.0.0.0:8000
