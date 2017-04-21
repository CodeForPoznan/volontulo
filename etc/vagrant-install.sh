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
DB_NAME=volontulo
DB_USERNAME=volontulo
DB_PASSWD=volontulo
su - postgres -c "psql -c 'CREATE ROLE $DB_USERNAME;'"
su - postgres -c "psql -c \"ALTER USER $DB_USERNAME with password '$DB_PASSWD';\""
su - postgres -c "psql -c \"ALTER ROLE $DB_USERNAME WITH LOGIN;\""
su - postgres -c "psql -c \"CREATE DATABASE $DB_NAME WITH  TEMPLATE=template0 ENCODING='utf-8' owner $DB_USERNAME;\""
cd /home/ubuntu/backend
python3 manage.py migrate --settings=volontulo_org.settings.dev_vagrant
python3 manage.py loaddata initial/data.json --settings=volontulo_org.settings.dev_vagrant

# # Finish
# cat << "EOF"

# ///     #//(  &(//////#    //(          (//////#@    (///    (/(  //////////( ///     (//   ///         &(//////#
# #//(    ///  /////#/////#  //(        ///////////(   (////   (/(     #//#     ///     (//   ///        ////// ////#
#  (//%  #//( (////( (#////% //(       (///#%/# (///#  (/////& (/(     #//#     ///     (//   ///       (/////# /////
#   /// %//(  ///%/    %///( //(        /(&@&( #(& /(  (// ///&(/(     #//#     (//     (//   ///       ///#     #///
#   #/////(   (///#    ////  //(         #///%(&/////  (//  (////(     #//#     (//     (//   ///       #///      (//
#    /////     ()#///(&///   //(&&&&&&@   #////////    (//   #///(     #//#     #///#////     ///&&&&@   #///(((((//

# EOF
