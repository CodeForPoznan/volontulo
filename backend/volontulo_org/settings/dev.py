"""
Development Settings Module
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DEBUG_TOOLBAR_PATCH_SETTINGS = False

INSTALLED_APPS += (
    'debug_toolbar',
    'django_coverage',
    'django_extensions',
    'django_nose',
    'corsheaders',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'fake_emails')

ANGULAR_ROOT = 'http://localhost:4200'

CORS_ORIGIN_WHITELIST = (
    'localhost:4200',
)
CORS_ALLOW_CREDENTIALS = True

SYSTEM_DOMAIN = 'localhost'
