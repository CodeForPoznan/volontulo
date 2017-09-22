#!/bin/bash -e

apt-get update -y
apt-get build-dep -y python-imaging
apt-get install -y python3-pip \
                   python-virtualenv \
                   libjpeg8 \
                   libjpeg62-dev \
                   libfreetype6 \
                   libfreetype6-dev \
                   libpq-dev \
                   wget

# install Google Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
apt-get update -y
apt-get install -y google-chrome-stable
