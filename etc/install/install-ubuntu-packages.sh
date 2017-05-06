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
