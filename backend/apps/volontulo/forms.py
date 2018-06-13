# -*- coding: utf-8 -*-

"""
.. module:: forms
"""

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.volontulo.utils import get_administrators_emails


class EditProfileForm(forms.Form):

    """Form reposponsible for edit user details on profile page."""
    first_name = forms.CharField(
        label="Imię",
        max_length=128,
        required=False
    )
    last_name = forms.CharField(
        label="Nazwisko",
        max_length=128,
        required=False
    )
    phone_no = forms.CharField(
        label="Numer telefonu",
        required=False
    )
    current_password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Aktualne hasło',
        required=False
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Nowe hasło",
        required=False
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Powtórz nowe hasło",
        required=False
    )
    user = forms.CharField(widget=forms.HiddenInput())

    def is_valid(self):
        valid = super(EditProfileForm, self).is_valid()
        if not valid:
            return valid

        current_password = self.cleaned_data['current_password']
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']
        user = User.objects.get(id=self.cleaned_data['user'])

        if (
                current_password and
                new_password and
                confirm_new_password
        ):
            if not user.check_password(current_password):
                raise ValidationError("Aktualne hasło jest błędne")

            if new_password != confirm_new_password:
                raise ValidationError("Wprowadzone hasła różnią się")

        return True


class OfferApplyForm(forms.Form):

    """Form for applying for join to offer ."""
    email = forms.CharField(max_length=80)
    phone_no = forms.CharField(max_length=80)
    fullname = forms.CharField(max_length=80)
    comments = forms.CharField(required=False, widget=forms.Textarea)


class ContactForm(forms.Form):

    """Basic contact form."""
    email = forms.CharField(max_length=150)
    message = forms.CharField(widget=forms.Textarea())
    name = forms.CharField(max_length=150)
    phone_no = forms.CharField(max_length=150)


class VolounteerToOrganizationContactForm(ContactForm):

    """Contact form specified for volounteers to mail to organization."""
    organization = forms.CharField(widget=forms.HiddenInput())


class AdministratorContactForm(ContactForm):

    """Contact form specified for anyone to mail to administrator."""
    APPLICANTS = (
        ('VOLUNTEER', 'wolontariusz'),
        ('ORGANIZATION', 'organizacja'),
    )
    applicant = forms.Select(choices=APPLICANTS)

    def __init__(self, *args, **kwargs):
        """Administrator contant form initialization.

        Administrator choice need to be here, as new Django release tries to
        import this form during migrations, even if user table is not
        available.
        """
        super(AdministratorContactForm, self).__init__(*args, **kwargs)
        self.administrator = forms.Select(
            choices=get_administrators_emails().items(),
        )
