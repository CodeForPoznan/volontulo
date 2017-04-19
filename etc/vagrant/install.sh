#!/bin/bash
# Script to set up a Django project on Vagrant.
PROJECT_NAME=$1

DB_NAME=$PROJECT_NAME
DB_USERNAME=$PROJECT_NAME
DB_PASSWD=$PROJECT_NAME

PROJECT_DIR=/home/vagrant/$PROJECT_NAME


# Install essential packages from Apt
apt-get update -y


# Python dev packages
apt-get build-dep -y python-imaging
apt-get install -y python3-pip \
        libjpeg8 \
        libjpeg62-dev \
        libfreetype6 \
        libfreetype6-dev \
        libpq-dev \
        wget


# Postgresql
if ! command -v psql; then
    apt-get install -y postgresql
fi


# install python packages
su - -c "pip3 install -r $PROJECT_DIR/requirements/dev.txt"

cp $PROJECT_DIR/local_config.yaml.sample $PROJECT_DIR/local_config.yaml
sed '/^secret_key/ d' $PROJECT_DIR/local_config.yaml > $PROJECT_DIR/tmp.yaml && mv tmp.yaml local_config.yaml
UUID=a63eb5ef-3b25-4595-846a-5d97d99486f0
echo "secret_key: $UUID" >> $PROJECT_DIR/local_config.yaml


# postgresql setup for project
su - postgres -c "psql -c 'CREATE ROLE $DB_USERNAME;'"
su - postgres -c "psql -c \"ALTER USER $DB_USERNAME with password '$DB_PASSWD';\""
su - postgres -c "psql -c \"ALTER ROLE $DB_USERNAME WITH LOGIN;\""
su - postgres -c "psql -c \"CREATE DATABASE $DB_NAME WITH  TEMPLATE=template0 ENCODING='utf-8' owner $DB_USERNAME;\""


# Django project setup
python3 $PROJECT_DIR/manage.py migrate --settings=volontulo_org.settings.dev_vagrant
python3 $PROJECT_DIR/manage.py loaddata $PROJECT_DIR/initial/data.json --settings=volontulo_org.settings.dev_vagrant


# Instrall nodejs
NODE_VERSION="7.4.0"
NVM_DIR="/home/vagrant/.nvm"

su - vagrant -c "wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.32.1/install.sh | bash"
source $NVM_DIR/nvm.sh
nvm install $NODE_VERSION &> /dev/null
nvm alias default $NODE_VERSION
nvm use default


# Install npm packages
cd $PROJECT_DIR/apps/volontulo && \
   npm install && \
   npm install gulp && \
   npm rebuild node-sass && \
   node node_modules/.bin/gulp build


# Finish
cat << "EOF"

///     #//(  &(//////#    //(          (//////#@    (///    (/(  //////////( ///     (//   ///         &(//////#
#//(    ///  /////#/////#  //(        ///////////(   (////   (/(     #//#     ///     (//   ///        ////// ////#
 (//%  #//( (////( (#////% //(       (///#%/# (///#  (/////& (/(     #//#     ///     (//   ///       (/////# /////
  /// %//(  ///%/    %///( //(        /(&@&( #(& /(  (// ///&(/(     #//#     (//     (//   ///       ///#     #///
  #/////(   (///#    ////  //(         #///%(&/////  (//  (////(     #//#     (//     (//   ///       #///      (//
   /////     ()#///(&///   //(&&&&&&@   #////////    (//   #///(     #//#     #///#////     ///&&&&@   #///(((((//

EOF
