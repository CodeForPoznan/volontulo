# -*- coding: utf-8 -*-

"""
.. module:: __init__
"""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render

from apps.volontulo.forms import AdministratorContactForm
from apps.volontulo.forms import EditProfileForm
from apps.volontulo.forms import UserGalleryForm
from apps.volontulo.lib.email import send_mail
from apps.volontulo.models import Offer
from apps.volontulo.models import UserProfile


def logged_as_admin(request):
    """Helper function that provide information is user has admin privilege.

    It is used in separate modules.

    :param request: WSGIRequest instance
    """
    return (
        request.user.is_authenticated() and
        UserProfile.objects.get(user=request.user).is_administrator
    )


def homepage_redirect(request):  # pylint: disable=unused-argument
    """Temporary redirect to old homepage."""
    return redirect('{}/{}'.format(settings.ANGULAR_ROOT, 'index.html'))


def homepage(request):
    """Main view of app.

    We will display page with few step CTA links?

    :param request: WSGIRequest instance
    """
    if logged_as_admin(request):
        offers = Offer.objects.get_for_administrator()
    else:
        offers = Offer.objects.get_weightened()

    return render(
        request,
        'homepage.html',
        {
            'offers': offers,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )


@login_required
def logged_user_profile(request):
    """View to display user profile page.

    :param request: WSGIRequest instance
    """
    def _init_edit_profile_form():
        """Initialize EditProfileForm - helper method."""
        return EditProfileForm(
            initial={
                'phone_no': request.user.userprofile.phone_no,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'user': request.user.id,
            }
        )

    def _populate_participated_offers(request):
        """Populate offers that current user participate."""
        return Offer.objects.filter(volunteers=request.user)

    def _populate_created_offers(request):
        """Populate offers that current user create."""
        return Offer.objects.filter(
            organization__userprofiles__user=request.user
        )

    def _is_saving_user_avatar():
        """."""
        return request.POST.get('submit') == 'save_image' and request.FILES

    def _is_saving_profile():
        """."""
        return request.POST.get('submit') == 'save_profile'

    def _save_userprofile():
        """Save user profile."""
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            if (
                    form.cleaned_data['current_password'] and
                    form.cleaned_data['new_password'] and
                    form.cleaned_data['confirm_new_password']
            ):
                user.set_password(form.cleaned_data['new_password'])
            user.userprofile.phone_no = form.cleaned_data['phone_no']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.userprofile.save()
            user.save()
            messages.success(
                request,
                'Zaktualizowano profil'
            )
        else:
            errors = '<br />'.join(form.errors)
            messages.error(
                request,
                'Problem w trakcie zapisywania profilu: {errors}'.format(
                    errors=errors
                )
            )
        return form

    def _handle_user_avatar_upload():
        """Handle image upload for user profile page."""
        gallery_form = UserGalleryForm(request.POST, request.FILES)
        if gallery_form.is_valid():
            userprofile.clean_images()
            gallery = gallery_form.save(commit=False)
            gallery.userprofile = userprofile
            # User can only change his avatar
            gallery.is_avatar = True
            gallery.save()
            messages.success(request, 'Dodano grafikę')
        else:
            errors = '<br />'.join(gallery_form.errors)
            messages.error(
                request,
                'Problem w trakcie dodawania grafiki: {errors}'.format(
                    errors=errors
                )
            )

    profile_form = _init_edit_profile_form()
    userprofile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        if _is_saving_user_avatar():
            _handle_user_avatar_upload()
        elif _is_saving_profile():
            profile_form = _save_userprofile()

    ctx = dict(
        profile_form=profile_form,
        user_avatar_form=UserGalleryForm(),
        userprofile=userprofile,
        MEDIA_URL=settings.MEDIA_URL
    )
    ctx['participated_offers'] = _populate_participated_offers(request)
    ctx['created_offers'] = _populate_created_offers(request)

    return render(request, 'users/user_profile.html', ctx)


def contact_form(request):
    """View responsible for contact forms.

    :param request: WSGIRequest instance
    """
    if request.method == 'POST':
        form = AdministratorContactForm(request.POST)
        if form.is_valid():
            # get administrators by IDS
            administrator_id = request.POST.get('administrator')
            admin = User.objects.get(id=administrator_id)
            send_mail(
                request,
                'contact_to_admin',
                [
                    admin.email,
                    request.POST.get('email'),
                ],
                {k: v for k, v in request.POST.items()},
            )
            messages.success(request, 'Email został wysłany.')
        else:
            errors = '<br />'.join(form.errors)
            messages.error(
                request,
                'Proszę poprawić błędy w formularzu: ' + errors
            )
            return render(
                request,
                'contact.html',
                {
                    'contact_form': form,
                }
            )

    form = AdministratorContactForm()
    return render(
        request,
        'contact.html',
        {
            'contact_form': form,
        }
    )


def page_not_found(request):
    """Page not found - 404 error handler.

    :param request: WSGIRequest instance
    """
    return render(
        request,
        '404.html',
        status=404
    )


def server_error(request):
    """Internal Server Error - 500 error handler.

    :param request: WSGIRequest instance
    """
    return render(
        request,
        '500.html',
    )
