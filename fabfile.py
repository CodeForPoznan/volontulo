# -*- coding: utf-8 -*-

u"""
.. module:: fabfile

Be aware, that becaus fabric doesn't support py3k You need to execute this
particular script using Python 2.
"""

import contextlib
import os
import sys

from fabric.api import cd
from fabric.api import env
from fabric.api import execute
from fabric.api import prefix
from fabric.api import run
from fabric.contrib import files


NODE_VERSION = '9.3.0'

env.user = 'root'
if not env.hosts:
    env.hosts = ['dev.volontulo.pl']
env.forward_agent = True

env_vars = {
    'dev.volontulo.pl': {
        'git_branch': 'master',
        'django_settings': 'dev_volontulo_pl',
    },
    'rc.volontulo.pl': {
        'git_branch': 'rc',
        'django_settings': 'rc_volontulo_pl',
    },
    'volontulo.pl': {
        'git_branch': 'prod',
        'django_settings': 'volontulo_pl',
    },
}


def update():
    u"""Function defining all steps required to properly update application."""

    # Django app refresh:
    with cd('/var/www/volontulo'):
        run('git checkout -f {}'.format(env_vars[env.host_string]['git_branch']))
        run('git pull')

    with contextlib.nested(
        prefix('workon volontulo'),
        cd('/var/www/volontulo/backend'),
    ):
        run('pip install --upgrade -r requirements/base.txt')

    # Django site refresh:
    with contextlib.nested(
        cd('/var/www/volontulo/backend'),
        prefix('workon volontulo')
    ):
        run('python manage.py migrate --traceback')

    # Angular assets refresh:
    with contextlib.nested(
        prefix('nvm use {}'.format(NODE_VERSION)),
        cd('/var/www/volontulo/frontend'),
    ):
        run('npm install .')
        run('./node_modules/.bin/ng build --prod --env={}'.format(env.host_string))
        run('./node_modules/.bin/ng build --prod --env={} --app 1 --output-hashing=false'.format(env.host_string))
        run('./node_modules/.bin/webpack --config webpack.server.config.js --progress --colors')

    run('systemctl restart uwsgi.service')
    run('systemctl restart nginx')
    run('systemctl restart pm2-www-data.service')


def install():
    u"""Function defining all steps required to install application."""

    # ensure that we have secrets configured:
    sys.path.insert(0, os.path.dirname(__file__))
    try:
        from secrets import (
            CFP_ADMIN_PASSWORD,
            VOLONTULO_SENTRY_DSN,
            WRK_ADMIN_PASSWORD,
        )
    except ImportError:
        print("Missing secrets")
        raise

    # Sytem upgrade:
    run('apt-get update -y')
    run('apt-get -o Dpkg::Options::="--force-confold" upgrade -y')
    run('apt-get install -y python-minimal')  # <- old fronted npm install requires python 2 executable

    # Secrets:
    run('apt-get install -y pwgen')
    run('echo "export VOLONTULO_SECRET_KEY=\"`pwgen 64 1`\"" >> ~/.bash_profile')
    run('echo "export VOLONTULO_DB_PASS=\"`pwgen 64 1`\"" >> ~/.bash_profile')
    run('source ~/.bash_profile')

    # Databse:
    run('apt-get install -y postgresql postgresql-contrib')
    run('su - postgres -c "psql -c \'CREATE ROLE volontulo;\'"')
    run('su - postgres -c "psql -c \\\\"ALTER USER volontulo with password \'$VOLONTULO_DB_PASS\';\\\\""')
    run('su - postgres -c "psql -c \'ALTER ROLE volontulo WITH LOGIN;\'"')
    run('su - postgres -c "psql -c \\\\"CREATE DATABASE volontulo WITH  TEMPLATE=template0 ENCODING=\'utf-8\' owner volontulo;\\\\""')

    # Mail Transport Agent:
    run('debconf-set-selections <<< "postfix postfix/mailname string $HOSTNAME"')
    run('debconf-set-selections <<< "postfix postfix/main_mailer_type string \'Internet Site\"')
    run('apt-get install -y postfix')

    # Fetch Volontulo code:
    run('apt-get install -y nginx')
    with cd('/var/www'):
        run('git clone https://github.com/CodeForPoznan/volontulo.git')
    with cd('/var/www/volontulo'):
        run('git checkout -f {}'.format(env_vars[env.host_string]['git_branch']))

    # Install proper Node:
    run('echo "export NVM_DIR=\"/var/www/.nvm\"" >> ~/.bash_profile')
    run('source ~/.bash_profile')
    run('wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash')
    run('echo \'[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"\' >> ~/.bash_profile')
    run('echo \'[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"\' >> ~/.bash_profile')
    run('source ~/.bash_profile')
    run('nvm install {}'.format(NODE_VERSION))

    # Install pm2
    with prefix('nvm use {}'.format(NODE_VERSION)):
        run('npm install -g pm2')
    with cd('/var'):
        run('chown www-data:www-data www')
    with contextlib.nested(
        prefix('nvm use {}'.format(NODE_VERSION)),
        cd('/var/www/volontulo/frontend'),
    ):
        run('npm install .')
        run('./node_modules/.bin/ng build --prod --env={}'.format(env.host_string))
        run('./node_modules/.bin/ng build --prod --env={} --app 1 --output-hashing=false'.format(env.host_string))
        run('./node_modules/.bin/webpack --config webpack.server.config.js --progress --colors')
        run("sudo -u www-data bash -c 'export PATH=/var/www/.nvm/versions/node/v{}/bin:$PATH && export HOME=/var/www  && export VOLONTULO_PM2_HOST=127.0.0.1 && pm2 start dist/server && pm2 save'".format(NODE_VERSION))
        run("env PATH=$PATH:/var/www/.nvm/versions/node/v{}/bin /var/www/.nvm/versions/node/v{}/lib/node_modules/pm2/bin/pm2 startup ubuntu -u www-data --hp /var/www".format(NODE_VERSION, NODE_VERSION))

    # Install virtualenv:
    run('apt-get install -y python3-pip')
    run('pip3 install --upgrade pip')
    run('pip3 install virtualenv virtualenvwrapper')
    run('echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bash_profile')
    run('echo "export WORKON_HOME=/var/www/virtualenvs" >> ~/.bash_profile')
    run('echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bash_profile')
    run('source ~/.bash_profile')
    run('mkvirtualenv volontulo')

    # Prepare Django application
    run('echo "export DJANGO_SETTINGS_MODULE=volontulo_org.settings.{}" >> ~/.bash_profile'.format(
        env_vars[env.host_string]['django_settings']))
    run('source ~/.bash_profile')
    with cd('/var/www/volontulo/backend'):
        run('mkdir media')
        run('chown www-data:www-data media')

    # Export Sentry DSN key
    run('echo "export VOLONTULO_SENTRY_DSN={}" >> ~/.bash_profile'.format(
        VOLONTULO_SENTRY_DSN))

    # Install uwsgi
    run('pip3 install uwsgi')
    run('mkdir -p /etc/uwsgi/sites')
    files.append('/etc/uwsgi/sites/volontulo.ini',
"""[uwsgi]
uid = www-data
chdir = /var/www/volontulo/backend
home = /var/www/virtualenvs/volontulo
module = volontulo_org.wsgi

env = DJANGO_SETTINGS_MODULE=volontulo_org.settings.{}""".format(
    env_vars[env.host_string]['django_settings']))
    run("echo 'env = VOLONTULO_SECRET_KEY='$VOLONTULO_SECRET_KEY >> /etc/uwsgi/sites/volontulo.ini")
    run("echo 'env = VOLONTULO_DB_PASS='$VOLONTULO_DB_PASS >> /etc/uwsgi/sites/volontulo.ini")
    run("echo 'env = VOLONTULO_SENTRY_DSN='$VOLONTULO_SENTRY_DSN >> /etc/uwsgi/sites/volontulo.ini")
    files.append('/etc/uwsgi/sites/volontulo.ini',
"""
socket = /run/uwsgi/volontulo.sock
chown-socket = www-data:www-data
chmod-socket = 660
vacuum = true
enable-threads = true
""")
    files.append('/etc/systemd/system/uwsgi.service',
"""[Unit]
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
""")
    run('systemctl start uwsgi')

    # Connect nginx with uwsgi:
    run('rm /etc/nginx/sites-enabled/default')
    files.append('/etc/nginx/sites-enabled/default',
"""server {{
    listen 80 default_server;
    listen [::]:80 default_server;

    if ($host != "{0}") {{
        return 301 https://{0}$request_uri;
    }}

}}

server {{
    charset utf-8;

    listen 80;
    listen [::]:80;

    listen 443 ssl;
    listen [::]:443 ssl;

    server_name {0};

    root /var/www/volontulo/frontend/dist/browser;
    index index.html;

    location /static/ {{
        root /var/www/volontulo/backend;
    }}

    location /media/ {{
        root /var/www/volontulo/backend;
    }}

    location = /o {{
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/volontulo.sock;
    }}

    location /o/ {{
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/volontulo.sock;
    }}

    location /api/ {{
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/volontulo.sock;
    }}

    location /admin {{
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/volontulo.sock;
    }}

    location / {{
        proxy_pass http://localhost:4200;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }}
}}
""".format(env.host_string))

    # Install SSL:
    run('add-apt-repository -y ppa:certbot/certbot')
    run('apt-get update -y')
    run('apt-get install -y python-certbot-nginx ')
    run('certbot --authenticator standalone --installer nginx -m hello@codeforpoznan.pl --agree-tos --no-eff-email -d {} --redirect --pre-hook "service nginx stop" --post-hook "service nginx start"'.format(env.host_string))
    run('(crontab -l 2>/dev/null; echo \'0 0 * * * certbot renew --post-hook "systemctl reload nginx"\') | crontab -')

    execute(update)

    # Create Django admin:
    with contextlib.nested(
        prefix('workon volontulo'),
        cd('/var/www/volontulo/backend'),
    ):
        run('python manage.py create_admin hello@codeforpoznan.pl {} --django-admin'.format(CFP_ADMIN_PASSWORD))
        run('python manage.py create_admin wolontariat@wrk.org.pl {}'.format(WRK_ADMIN_PASSWORD))
