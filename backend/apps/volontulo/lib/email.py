# -*- coding: utf-8 -*-

"""
.. module:: email
"""

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection
from django.template.loader import get_template

from apps.volontulo.utils import get_administrators_emails

FROM_ADDRESS = 'no-reply@' + settings.SYSTEM_DOMAIN
FAIL_SILENTLY = False
AUTH_USER = None
AUTH_PASSWORD = None
CONNECTION = None

SUBJECTS = {
    'offer_application': 'Zgłoszenie chęci pomocy w ofercie',
    'offer_creation': 'Zgłoszenie oferty na Volontulo',
    'registration': 'Rejestracja na Volontulo',
    'contact_to_admin': 'Kontakt z administratorem',
    'volunteer_to_organisation': 'Kontakt od wolontariusza',
}


def send_mail(request, templates_name, recipient_list, context=None):
    """Proxy for sending emails."""
    fail_silently = FAIL_SILENTLY
    auth_user = AUTH_USER
    auth_password = AUTH_PASSWORD
    connection = CONNECTION

    context = context or {}
    context.update({
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': get_current_site(request).domain,
    })
    text_template = get_template('emails/{}.txt'.format(templates_name))
    html_template = get_template('emails/{}.html'.format(templates_name))

    bcc = list(get_administrators_emails().values())
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently
    )
    # required, if omitted then no emails from BCC are send
    headers = {'bcc': ','.join(bcc)}
    email = EmailMultiAlternatives(
        SUBJECTS[templates_name],
        text_template.render(context),
        FROM_ADDRESS,
        recipient_list,
        bcc,
        connection=connection,
        headers=headers
    )
    email.attach_alternative(html_template.render(context), 'text/html')

    return email.send()
