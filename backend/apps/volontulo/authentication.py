"""
.. module::authentication
"""

from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Hack do prevent CSRF in API"""

    def enforce_csrf(self, request):
        """Mock CSRF validation"""
        return  # To not perform the csrf check previously happening
