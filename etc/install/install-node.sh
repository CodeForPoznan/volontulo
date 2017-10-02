#!/bin/bash -e

wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
source $NVM_DIR/nvm.sh
nvm install $NODE_VERSION
nvm alias default $NODE_VERSION
nvm use default


echo "export NVM_DIR=\"$NVM_DIR\"" >> $USER_DIR/.bash_profile
echo '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"' >> $USER_DIR/.bash_profile
