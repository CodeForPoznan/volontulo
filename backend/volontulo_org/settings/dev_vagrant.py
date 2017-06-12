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
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
