"""
Development Settings Module
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    'backend',
]

INSTALLED_APPS += (
    'django_coverage',
    'django_extensions',
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'fake_emails')

ANGULAR_ROOT = 'http://localhost:4200'

SYSTEM_DOMAIN = 'localhost'

LOGIN_URL = '{}/login'.format(ANGULAR_ROOT)
