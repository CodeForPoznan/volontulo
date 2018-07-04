# pylint: disable=no-self-use
from django.test import TransactionTestCase
from rest_framework.exceptions import ValidationError

from apps.volontulo.factories import UserFactory
from apps.volontulo.validators import validate_admin_email


class TestAdminEmailValidator(TransactionTestCase):

    def test_raises_error_if_user_does_not_exist(self):
        email = 'john@snow.got'
        with self.assertRaises(
            ValidationError,
            msg='Administrator o adresie e-mail {} nie istnieje.'.format(
                email,
            ),
        ):
            validate_admin_email(email)

    def test_raises_error_if_user_is_not_admin(self):
        user = UserFactory.create(userprofile__is_administrator=False)

        with self.assertRaises(
            ValidationError,
            msg='Administrator o adresie e-mail {} nie istnieje.'.format(
                user.email,
            ),
        ):
            validate_admin_email(user.email)

    def test_does_not_raise_error_if_user_is_admin(self):
        user = UserFactory.create(userprofile__is_administrator=True)

        try:
            validate_admin_email(user.email)
        except ValidationError:
            self.fail('raised error when user is admin')
