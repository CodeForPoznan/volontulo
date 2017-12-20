FROM ubuntu:16.04

# Expose network ports
EXPOSE 8000
EXPOSE 4200

# Add build-time directories
ADD etc /volontulo/etc
ADD backend /volontulo/backend
ADD frontend /volontulo/frontend
WORKDIR /volontulo

# Docker-based quirks
ENV LANG C.UTF-8
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN echo "deb-src http://archive.ubuntu.com/ubuntu/ xenial main restricted" >> /etc/apt/sources.list

# Distinct (Docker vs Vagrant) env variables
ENV NODE_VERSION 9.3.0
ENV NVM_DIR /usr/local/nvm
ENV NODE_PATH $NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
ENV USER_DIR="/root"
ENV BACKEND_DIR /volontulo/backend
ENV FRONTEND_DIR /volontulo/frontend

# Common (Docker & Vagrant) setup
RUN ./etc/install/install-ubuntu-packages.sh
RUN ./etc/install/install-node.sh
RUN ./etc/install/setup-backend.sh
RUN ./etc/install/setup-old-frontend.sh
RUN ./etc/install/setup-frontend.sh

# Setup wait-for-it for docker-compose
RUN wget -qO /usr/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod a+x /usr/bin/wait-for-it
