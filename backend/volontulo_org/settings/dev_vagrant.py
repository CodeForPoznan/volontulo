"""
Vagrant Development Settings Module
"""

from .dev import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'volontulo',
        'USER': 'volontulo',
        'PASSWORD': 'volontulo',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
