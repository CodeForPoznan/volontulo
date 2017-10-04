#!/bin/bash

# Distinct (Docker vs Vagrant) env variables
export NODE_VERSION="7.9.0"
export NVM_DIR="/home/ubuntu/.nvm"
export NODE_PATH="$NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules"
export PATH="$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH"
export USER_DIR="/home/ubuntu"
export BACKEND_DIR="/home/ubuntu/backend"
export FRONTEND_DIR="/home/ubuntu/frontend"

# Common (Docker & Vagrant) setup
./etc/install/install-ubuntu-packages.sh
./etc/install/install-node.sh
./etc/install/setup-backend.sh
./etc/install/setup-old-frontend.sh
./etc/install/setup-frontend.sh

# Setup Postgresql and populate database
if ! command -v psql; then
    apt-get install -y postgresql
fi

export VOLONTULO_DB_USER="volontulo"
export VOLONTULO_DB_PASS="volontulo"
export VOLONTULO_DB_NAME="volontulo"
su - postgres -c "psql -c 'CREATE ROLE $VOLONTULO_DB_USER;'"
su - postgres -c "psql -c \"ALTER USER $VOLONTULO_DB_USER with password '$VOLONTULO_DB_PASS';\""
su - postgres -c "psql -c \"ALTER ROLE $VOLONTULO_DB_USER WITH LOGIN;\""
su - postgres -c "psql -c \"CREATE DATABASE $VOLONTULO_DB_NAME WITH  TEMPLATE=template0 ENCODING='utf-8' owner $VOLONTULO_DB_USER;\""

cd /home/ubuntu/backend
export DJANGO_SETTINGS_MODULE="volontulo_org.settings.dev"
export VOLONTULO_SECRET_KEY="a63eb5ef-3b25-4595-846a-5d97d99486f0"
python3 manage.py migrate
python3 manage.py loaddata initial/data.json


echo "export DJANGO_SETTINGS_MODULE=\"$DJANGO_SETTINGS_MODULE\"" >> /home/ubuntu/.bash_profile
echo "export VOLONTULO_DB_PASS=\"$OLONTULO_DB_PASS\"" >> /home/ubuntu/.bash_profile
echo "export VOLONTULO_SECRET_KEY=\"$VOLONTULO_SECRET_KEY\"" >> /home/ubuntu/.bash_profile
