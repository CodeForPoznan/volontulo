# -*- coding: utf-8 -*-

u"""
.. module:: fabfile

Be aware, that becaus fabric doesn't support py3k You need to execute this
particular script using Python 2.
"""

import contextlib

from fabric.api import cd
from fabric.api import env
from fabric.api import prefix
from fabric.api import run

env.user = 'root'
env.hosts = ['volontuloapp.org']
env.forward_agent = True


def update():
    u"""Function defining all steps required to properly update application."""

    # Django app refresh:
    with cd('/var/www/volontuloapp_org'):
        run('git checkout master')
        run('git pull')

    with contextlib.nested(
        prefix('workon volontuloapp_org'),
        cd('/var/www/volontuloapp_org/backend'),
    ):
        run('pip install --upgrade -r requirements/base.txt')

    # Gulp frontend refresh:
    with contextlib.nested(
        prefix('nvm use 7.9.0'),
        cd('/var/www/volontuloapp_org/backend/apps/volontulo'),
    ):
        run('npm install .')
        run('node node_modules/.bin/gulp build')

    # Django site refresh:
    with contextlib.nested(
        cd('/var/www/volontuloapp_org/backend'),
        prefix('workon volontuloapp_org')
    ):
        run('python manage.py migrate --traceback')
        run('python manage.py collectstatic --traceback --noinput')

    # Angular assets refresh:
    with contextlib.nested(
        prefix('nvm use 7.9.0'),
        cd('/var/www/volontuloapp_org/frontend'),
    ):
        run('npm install .')
        run('ng build --prod')
        run('service apache2 restart')
