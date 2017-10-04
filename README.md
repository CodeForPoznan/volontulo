# Volontulo

[![Join the chat at https://gitter.im/CodeForPoznan/volontulo](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/CodeForPoznan/volontulo?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/CodeForPoznan/volontulo.svg)](https://travis-ci.org/CodeForPoznan/volontulo)
[![codecov.io](http://codecov.io/github/CodeForPoznan/volontulo/coverage.svg?branch=master)](http://codecov.io/github/CodeForPoznan/volontulo?branch=master)

![Volontulo logo](/backend/apps/volontulo/frontend/img/volo_logo.png)

Web portal for collaboration of community volunteers with organizations and institutions. 

## Developer setup

For developers' convenience we are supporting two widely used virtualization platforms: **Docker** and **Vagrant**.

### Docker

To run our application in development mode You need to have **Docker** and **Docker Compose**.

That's the easiest way to setup environment - from downloaded source code run
```
docker-compose up
```
and point your browser to [http://localhost:8000](http://localhost:8000) and [http://localhost:4200](http://localhost:4200)

### Vagrant

To run our application in Vagrant:

* provision and start Vagrant container
```
vagrant up
```
* SSH into it (do it twice, for backend and frontend)
```
vagrant ssh
```
* run backend
```
cd /home/ubuntu/backend
python3 manage.py runserver 0.0.0.0:8000
```
* run frontend
```
cd /home/ubuntu/frontend
ng serve --open --host=0.0.0.0
```
* point your browser to [http://localhost:8000](http://localhost:8000) and [http://localhost:4200](http://localhost:4200)

### Manual project set up

For manual installation You can follow `Dockerfile`/`etc/vagrant-install.sh` instructions.

For Your convenience we suggest to use **virtualenv** and `backend/volontulo_org/settings/dev_local.py` (as it use SQLite instead of PostgreSQL).

## Initial admin credentials
 * **user**: admin@volontuloapp.org
 * **pass**: stx123
