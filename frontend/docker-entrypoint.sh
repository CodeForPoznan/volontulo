#!/bin/bash
set -e

npm install
node_modules/.bin/ng serve --open --host=0.0.0.0 --proxy docker-dev-proxy.json

