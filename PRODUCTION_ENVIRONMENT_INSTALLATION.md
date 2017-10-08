# Production environment installation

## Prerequisites

1. We have `root` access to new VPS server with Ubuntu 16.04 preinstalled.
1. Proper domain (`dev.volontulo.pl`, `rc.volontulo.pl` or `volontulo.pl`) was redirected into new VPS's IP address.

## Update and upgrade

1. Start from updating repositories and upgrading system:
```
apt-get update
apt-get upgrade
```

## Secrets as environment variables

1. Install `pwgen` for generating random secrets.
```
apt-get install pwgen
```
2. Establish environment variables (VOLONTULO_SECRET_KEY and VOLONTULO_DB_PASS) that will handle our secrets and add them to root's `.bash_profile`:
```
echo "export VOLONTULO_SECRET_KEY=\"`pwgen 64 1`\"" >> ~/.bash_profile
echo "export VOLONTULO_DB_PASS=\"`pwgen 64 1`\"" >> ~/.bash_profile
source ~/.bash_profile
```

## Database

This part is based on https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04

1. Install PostgreSQL packages:
```
apt-get install postgresql postgresql-contrib
```
2. Create user and database for application (as default we create user named **volontulo** and database named **volontulo**):
```
su - postgres -c "psql -c 'CREATE ROLE volontulo;'"
su - postgres -c "psql -c \"ALTER USER volontulo with password '$VOLONTULO_DB_PASS';\""
su - postgres -c "psql -c 'ALTER ROLE volontulo WITH LOGIN;'"
su - postgres -c "psql -c \"CREATE DATABASE volontulo WITH  TEMPLATE=template0 ENCODING='utf-8' owner volontulo;\""
```

## Mail Transport Agent

This part is based on http://cheng.logdown.com/posts/2015/06/08/django-send-email-using-postfix

1. Install Posftix packages:
```
sudo apt-get install postfix
```
2. During installation choose **Internet Site**.
3. System mail name leave as it was.

## Fetch current Volontulo state

1. We will store all our files inside standard root for almost all webservers - `/var/www`. Just install **Nginx** to have this directory:
```
apt-get install nginx
```
2. Go to it and fetch current state of Volontulo repository:
```
cd /var/www
git clone https://github.com/CodeForPoznan/volontulo.git
```

## Install proper Node

1. Install **nvm**:
```
wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.5/install.sh | bash
```
2. Setup **nvm** environment variables:
```
echo "export NVM_DIR=\"$HOME/.nvm\"" >> ~/.bash_profile
echo '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"' >> ~/.bash_profile
echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> ~/.bash_profile
source ~/.bash_profile
```
3. Install Node **7.9** (that's the one, we use in docker, vagrant etc.):
```
nvm install 7.9
```

## Prepare old (Django-based) frontend

1. Go to directory `volontulo` app directory:
```
cd /var/www/volontulo/backend/apps/volontulo
```
2. Install npm dependencies:
```
npm install
```
3. Build old frontend using **gulp**:
```
./node_modules/gulp/bin/gulp.js build
```

## Prepare new (Angular-based) frontend

1. Go to frontend directory:
```
cd /var/www/volontulo/frontend
```
2. Install **angular-cli** globally (there's an issue with `uglifyjs-webpack-plugin`, see: https://stackoverflow.com/a/46482556):
```
npm install -g @angular/cli --unsafe-perm
```
3. Install npm dependencies:
```
npm install
```
4. Build Angular application for specific environment (choose from `dev.volontulo.pl`, `rc.volontulo.pl` and `volontulo.pl`, see: https://github.com/CodeForPoznan/volontulo/blob/master/frontend/.angular-cli.json#L28, also there's an issue with AOT compiler, see: https://github.com/angular/angular-cli/issues/4551#issuecomment-284224993):
```
ng build --prod --env=<CHOOSEN_ENVIRONMENT> --aot=false
```

## Install virtualenv for Django

1. Install pip from Ubuntu packages and upgrade it:
```
apt-get install python3-pip
pip3 install --upgrade pip
```
2. Install virtualenv and virtualenvwrapper:
```
pip3 install virtualenv virtualenvwrapper
```
3. Setup virtualenvwrapper (as we will use virtual environments in webserver, we will place them in `/var/www` directory):
```
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bash_profile
echo "export WORKON_HOME=/var/www/virtualenvs" >> ~/.bash_profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bash_profile
source ~/.bash_profile
```
4. Create virtual environment:
```
mkvirtualenv volontulo
```
5. Install Django dependencies:
```
pip install -r /var/www/volontulo/backend/requirements/base.txt
```

## Prepare Django application

1. Go to Django application directory:
```
cd /var/www/volontulo/backend
```
2. Add default settings module into environment variables (choose from `volontulo_org.settings.dev_volontulo_pl`, `volontulo_org.settings.rc_volontulo_pl` and `volontulo_org.settings.volontulo_pl)`:
```
echo "export DJANGO_SETTINGS_MODULE=<CHOSEN_SETTINGS_MODULE>" >> ~/.bash_profile
source ~/.bash_profile
```
3. Migrate models into database:
```
python manage.py migrate
```
4. Collect statics:
```
python manage.py collectstatic
```
5. Create `media` directory with proper permissions:
```
mkdir media
chown www-data:www-data media
```
6. Create Django admin (remember that it will not have `UserProfile`):
```
python manage.py createsuperuser
```

## Install and configure **uwsgi**

This part is based on https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-16-04 and https://coderwall.com/p/93jakg/multiple-env-vars-with-uwsgi

1. If You're in virtualenv, deactivate it:
```
deactivate
```
2. Install **uwsgi**:
```
pip3 install uwsgi
```
3. Setup sites configurations directory for **uwsgi**:
```
mkdir -p /etc/uwsgi/sites
```
4. Create volontulo **uwsgi** configuration file `/etc/uwsgi/sites/volontulo.ini` and paste to it (of course with appropriate secrets):
```
[uwsgi]
uid = www-data
chdir = /var/www/volontulo/backend
home = /var/www/virtualenvs/volontulo
module = volontulo_org.wsgi

env = DJANGO_SETTINGS_MODULE=<CHOSEN_SETTINGS_MODULE>
env = VOLONTULO_SECRET_KEY=<SECRET_KEY>
env = VOLONTULO_DB_PASS=<DB_PASS>

socket = /run/uwsgi/volontulo.sock
chown-socket = www-data:www-data
chmod-socket = 660
vacuum = true
```
5. Create systemd-based service for **uwsgi** (`/etc/systemd/system/uwsgi.service`) and paste to it:
```
[Unit]
Description=uWSGI Emperor service

[Service]
ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown www-data:www-data /run/uwsgi'
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```
6. Start **uwsgi** service:
```
systemctl start uwsgi
```

## Connect **nginx** with **wsgi**

1. Enable utf-8 in **nginx** - add to `http` section of `/etc/nginx/nginx.conf` line:
```
    charset utf-8;
```
2. Because we will serve Volontulo from specific domain change `/etc/nginx/sites-available/default` to redirect all traffic to this particular domain - add to `server` section lines (of course change domain name to proper one):
```
    if ($host != "<PROPER_DOMAIN_NAME>") {
        return 301 https://<PROPER_DOMAIN_NAME>$request_uri;
    }
```
3. Also in `/etc/nginx/sites-available/default` create new `server` section that will looks like (change domain name to proper one):
```
server {
    listen 80;
    listen [::]:80;

    listen 443 ssl;
    listen [::]:443 ssl;

    server_name <PROPER_DOMAIN_NAME>;

    root /var/www/volontulo/frontend/dist;
    index index.html;

    location /static/ {
        root /var/www/volontulo/backend;
    }

    location /media/ {
        root /var/www/volontulo/backend;
    }

    location = /o {
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/volontulo.sock;
    } 

    location /o/ {
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/volontulo.sock;
    }

    location /api/ {
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/volontulo.sock;
    }

    location /admin {
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/volontulo.sock;
    }

    location / {
        try_files $uri /index.html;
    }
}
```

## Install SSL certificate for website

This part is based on https://certbot.eff.org/#ubuntuxenial-nginx

1. Install **certbot**:
```
add-apt-repository ppa:certbot/certbot
apt-get update
apt-get install python-certbot-nginx 
```
2. Install certificate using:
```
certbot --nginx
```
3. During certificate's installation provide `hello@codeforpoznan.pl` email address, agree to ToS, don't share email eddress with EFF, choose proper domain (there should be only one), choose redirect. This step will add few lines to `/etc/nginx/sites-available/default`:
```
ssl_certificate /etc/letsencrypt/live/<PROPER_DOMAIN_NAME>/fullchain.pem; # managed by Certbot
ssl_certificate_key /etc/letsencrypt/live/<PROPER_DOMAIN_NAME>/privkey.pem; # managed by Certbot
```
and
```
    if ($scheme != "https") {
        return 301 https://$host$request_uri;
    } # managed by Certbot
```
4. Add cron task for certificate renewal - open crontab:
```
crontab -e
```
5. ...and add one line to renew certificate:
```
0 0 * * * certbot renew --post-hook "systemctl reload nginx"
```


## THE END!

1. Point your web browser on <PROPER_DOMAIN_NAME> and see working Volontulo!
