FROM ubuntu:16.04

ADD . /app

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update
RUN apt-get build-dep -y python-imaging
RUN apt-get install -y python3-pip \
                       libjpeg8 \
                       libjpeg62-dev \
                       libfreetype6 \
                       libfreetype6-dev \
                       wget

ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 4.2.0

RUN wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.31.4/install.sh | bash && \
    source $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use default

ENV NODE_PATH $NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements/dev.txt
RUN cp etc/local_config.yaml.sample local_config.yaml
RUN sed '/^secret_key/ d' local_config.yaml > tmp.yaml && mv tmp.yaml local_config.yaml

ENV SECRET_KEY=a63eb5ef-3b25-4595-846a-5d97d99486f0

RUN echo "secret_key: $SECRET_KEY" >> local_config.yaml
RUN python3 manage.py migrate --settings=volontulo_org.settings.dev
RUN python3 manage.py loaddata initial/data.json --settings=volontulo_org.settings.dev

WORKDIR /app/apps/volontulo

RUN npm install
RUN node node_modules/.bin/gulp build

WORKDIR /app

EXPOSE 8000

ENTRYPOINT python3 manage.py runserver --settings=volontulo_org.settings.dev 0.0.0.0:8000
