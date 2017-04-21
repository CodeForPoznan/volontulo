#!/bin/bash -e

cd $BACKEND_DIR/apps/volontulo
npm install
node ./node_modules/.bin/gulp build
cd -
