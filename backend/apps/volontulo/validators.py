"""Custom validators."""
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError


def validate_admin_email(email):
    """Validates if email is an e-mail belonging to site administrator."""
    user_model = get_user_model()
    try:
        user_model.objects.get(userprofile__is_administrator=True, email=email)
    except user_model.DoesNotExist:
        raise ValidationError(
            'Administrator o adresie e-mail {} nie istnieje.'.format(email),
        )
