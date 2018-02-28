"""
Settings specific to environment behind volontulo.pl.
"""
# pylint: skip=file

from .base import *

# Extra settings go here:

ANGULAR_ROOT = 'https://volontulo.pl'
SYSTEM_DOMAIN = 'volontulo.pl'

LOGIN_URL = '{}/login'.format(ANGULAR_ROOT)
