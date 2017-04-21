#!/bin/bash -e

pip3 install --upgrade pip
pip3 install -r $BACKEND_DIR/requirements/dev.txt
cp $BACKEND_DIR/local_config.yaml.sample $BACKEND_DIR/local_config.yaml
sed '/^secret_key/ d' $BACKEND_DIR/local_config.yaml > $BACKEND_DIR/tmp.yaml && mv $BACKEND_DIR/tmp.yaml $BACKEND_DIR/local_config.yaml
echo "secret_key: a63eb5ef-3b25-4595-846a-5d97d99486f0" >> $BACKEND_DIR/local_config.yaml
