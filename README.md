# Volontulo

[![Join the chat at https://gitter.im/CodeForPoznan/volontulo](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/CodeForPoznan/volontulo?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/CodeForPoznan/volontulo.svg)](https://travis-ci.org/CodeForPoznan/volontulo)
[![codecov.io](http://codecov.io/github/CodeForPoznan/volontulo/coverage.svg?branch=master)](http://codecov.io/github/CodeForPoznan/volontulo?branch=master)

![Volontulo logo](/frontend/src/assets/img/volo_logo.png)

Web portal for collaboration of community volunteers with organizations and institutions. 

## Developer setup

To run our application in development mode You need to have **Docker** and **Docker Compose**.

That's the easiest way to setup environment - from downloaded source code run
```
docker-compose up
```
and point your browser to [http://localhost:8000](http://localhost:8000) and [http://localhost:4200](http://localhost:4200)

## Initial admin credentials
We have 2 levels of admin users and 2 initial users - with and without Django Admin access:

username               | password | Django Admin access
---------------------- | -------- | -------------------
hello@codeforpoznan.pl | cfp123   | yes
wolontariat@wrk.org.pl | wrk123   | no

## Instances

* dev (https://dev.volontulo.pl)
* RC (https://rc.volontulo.pl)
* production (https://volontulo.pl)

## Release cycles definition

Working agreement:

* We work in 6-weeks sprints. Code is pushed to the dev instance after merging and passing tests.
* Code freeze at the end of the 5th week. Regression tests can be started after pushing the release branch to release candidate instance. 
* Regression lasts for one week and all of the regression bugs, that have been found, should be fixed with highest priority in week 6.
* Afterwards application is to be tested and approved by the client. 
* Sign-off from the client means that we push the code to the production after week 6.


## Responsive design breakpoints

Angular implementation use extensively Bootstrap 4 - we will comply with [standard Bootstrap 4 breakpoints described on its website](https://getbootstrap.com/docs/4.0/layout/overview/#responsive-breakpoints).

## Running tests locally

In order to run tests locally, execute one of the following commands:

```bash
make test_all  # backend and frontend tests
make test_backend  # backend tests + linter
make test_frontend  # frontend tests
```

They will run docker image from the corresponding service.
It will run in one-off mode but failed tests will leave a container behind - remember to clean it from time to time.
