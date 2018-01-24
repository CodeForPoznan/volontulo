FROM ubuntu:16.04

# Expose network ports
EXPOSE 8000

# Docker-based quirks
ENV LANG C.UTF-8
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN echo "deb-src http://archive.ubuntu.com/ubuntu/ xenial main restricted" >> /etc/apt/sources.list

# Docker env variables
ENV NODE_VERSION 9.3.0
ENV NVM_DIR /usr/local/nvm
ENV NODE_PATH $NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
ENV USER_DIR="/root"

# System-based package isntallation
RUN apt-get update -y
RUN apt-get install -y python3-pip \
                       python-virtualenv \
                       libpq-dev \
                       wget

# Backend setup
ADD requirements /volontulo/backend/requirements
WORKDIR /volontulo/backend
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements/dev.txt

# Old fronted setup
RUN wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
RUN . $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use default

# Setup wait-for-it for docker-compose
RUN wget -qO /usr/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod a+x /usr/bin/wait-for-it

# Add build-time directories
ADD . /volontulo/backend

WORKDIR /volontulo/backend/apps/volontulo
RUN npm install
RUN node ./node_modules/.bin/gulp build
WORKDIR /volontulo/backend
