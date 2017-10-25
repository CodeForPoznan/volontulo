# -*- coding: utf-8 -*-

u"""
.. module:: fabfile

Be aware, that becaus fabric doesn't support py3k You need to execute this
particular script using Python 2.
"""

import contextlib
import random
import string

from fabric.api import cd
from fabric.api import env
from fabric.api import execute
from fabric.api import prefix
from fabric.api import run
from fabric.contrib import files

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
        run('git checkout {}'.format(env_vars[env.host_string]['git_branch']))
        run('git pull')

    with contextlib.nested(
        prefix('workon volontulo'),
        cd('/var/www/volontulo/backend'),
    ):
        run('pip install --upgrade -r requirements/base.txt')

    # Gulp frontend refresh:
    with contextlib.nested(
        prefix('nvm use 7.9.0'),
        cd('/var/www/volontulo/backend/apps/volontulo'),
    ):
        run('npm install .')
        run('node node_modules/.bin/gulp build')

    # Django site refresh:
    with contextlib.nested(
        cd('/var/www/volontulo/backend'),
        prefix('workon volontulo')
    ):
        run('python manage.py migrate --traceback')
        run('python manage.py collectstatic --traceback --noinput')

    # Angular assets refresh:
    with contextlib.nested(
        prefix('nvm use 7.9.0'),
        cd('/var/www/volontulo/frontend'),
    ):
        run('npm install .')
        run('ng build --prod --env={} --aot=false'.format(env.host_string))

    run('systemctl restart uwsgi.service')
    run('systemctl restart nginx')


def install():
    u"""Function defining all steps required to install application."""

    # Sytem upgrade:
    run('apt-get update -y')
    run('apt-get -o Dpkg::Options::="--force-confold" upgrade -y')

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
        run('git checkout {}'.format(env_vars[env.host_string]['git_branch']))

    # Install proper Node:
    run('wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.5/install.sh | bash')
    run('echo "export NVM_DIR=\"$HOME/.nvm\"" >> ~/.bash_profile')
    run('echo \'[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"\' >> ~/.bash_profile')
    run('echo \'[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"\' >> ~/.bash_profile')
    run('source ~/.bash_profile')
    run('nvm install 7.9')
    with prefix('nvm use 7.9.0'):
        run('npm install -g @angular/cli --unsafe-perm')

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
    files.append('/etc/uwsgi/sites/volontulo.ini',
"""
socket = /run/uwsgi/volontulo.sock
chown-socket = www-data:www-data
chmod-socket = 660
vacuum = true
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

    root /var/www/volontulo/frontend/dist;
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
        try_files $uri /index.html;
    }}
}}
""".format(env.host_string))

    # Install SSL:
    run('add-apt-repository -y ppa:certbot/certbot')
    run('apt-get update -y')
    run('apt-get install -y python-certbot-nginx ')
    run('certbot --nginx -m hello@codeforpoznan.pl --agree-tos --no-eff-email -d {} --redirect'.format(env.host_string))
    run('(crontab -l 2>/dev/null; echo \'0 0 * * * certbot renew --post-hook "systemctl reload nginx"\') | crontab -')

    execute(update)

    # Create Django admin:
    with contextlib.nested(
        prefix('workon volontulo'),
        cd('/var/www/volontulo/backend'),
    ):
        django_admin_pass = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(64))
        run('echo "from django.contrib.auth import get_user_model; User = get_user_model(); u = User(username=\'admin\',, is_staff=True, is_superuser=True); u.set_password(\'{}\'); u.save()" | python manage.py shell'.format(django_admin_pass))
        print('Django Admin Password: {}'.format(django_admin_pass))
