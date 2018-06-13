# -*- coding: utf-8 -*-

"""
.. module:: offers
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.generic import View

from apps.volontulo.forms import OfferApplyForm
from apps.volontulo.lib.email import send_mail
from apps.volontulo.models import Offer
from apps.volontulo.models import UserProfile
from apps.volontulo.utils import correct_slug
from apps.volontulo.views import logged_as_admin


class OffersList(View):
    """View that handle list of offers."""

    @staticmethod
    def get(request):
        """It's used for volunteers to show active ones and for admins to show
        all of them.

        :param request: WSGIRequest instance
        """
        if logged_as_admin(request):
            offers = Offer.objects.all()
        else:
            offers = Offer.objects.get_active()

        return render(request, "offers/offers_list.html", context={
            'offers': offers,
        })

    @staticmethod
    def post(request):
        """Method responsible for rendering form for new offer.

        :param request: WSGIRequest instance
        """
        if (
                request.POST.get('edit_type') == 'status_change' and
                request.POST.get('offer_id')
        ):
            offer = get_object_or_404(Offer, id=request.POST.get('offer_id'))
            offer.publish()
            messages.success(request,
                             "Aktywowałeś ofertę '%s'" % offer.title)
        return redirect('offers_list')


class OffersReorder(View):
    """Class view supporting change of a offer."""

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if (
                not user.is_authenticated() or
                not user.userprofile.is_administrator
        ):
            return redirect('offers_list')
        return super(OffersReorder, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def get(request, id_):
        """Display offer list with weights GET request.

        :param request: WSGIRequest instance
        :param id_:
        :return:
        """
        offers = Offer.objects.get_weightened()
        return render(request, 'offers/reorder.html', {
            'offers': offers, 'id': id_})

    @staticmethod
    def post(request, _):
        """Display offer list with weights GET request.

        :param request:
        :param id_: Integer newly created offer id
        :return:
        """
        if request.POST.get('submit') == 'reorder':
            items = [item
                     for item
                     in request.POST.items()
                     if item[0].startswith('weight_')]
            weights = {id_.split('_')[1]: weight
                       for id_, weight in items}
            for id_, weight in weights.items():
                Offer.objects.filter(id=id_).update(weight=weight)

            messages.success(
                request,
                "Uporządkowano oferty."
            )
        return redirect('offers_list')


class OffersAccept(View):
    """ Class view responsible for acceptance of offers """

    @staticmethod
    def get(request, pk):  # pylint: disable=invalid-name
        """Method which allows to delete selected offer

        :param request: WSGIRequest instance
        :param pk: Offer id
        """
        offer = get_object_or_404(Offer, pk=pk)
        if (
                request.user.is_authenticated() and
                request.user.userprofile.is_administrator
        ):
            offer.publish()
            messages.info(request, "Oferta została zaakceptowana.")
            return redirect(settings.ANGULAR_ROOT)

        return HttpResponseForbidden()


class OffersJoin(View):
    """Class view supporting joining offer."""

    @staticmethod
    @correct_slug(Offer, 'offers_join', 'title')
    def get(request, slug, id_):  # pylint: disable=unused-argument
        """View responsible for showing join form for particular offer."""
        if request.user.is_authenticated():
            has_applied = Offer.objects.filter(
                volunteers=request.user,
                volunteers__offer=id_,
            ).count()
            if has_applied:
                messages.error(
                    request,
                    "Już wyraziłeś chęć uczestnictwa w tej ofercie."
                )
                return redirect('offers_list')

        offer = Offer.objects.get(id=id_)

        context = {
            'form': OfferApplyForm(),
            'offer': offer,
            'MEDIA_URL': settings.MEDIA_URL,
        }

        context['volunteer_user'] = UserProfile()
        if request.user.is_authenticated():
            context['volunteer_user'] = request.user.userprofile

        return render(
            request,
            'offers/offer_apply.html',
            context
        )

    @staticmethod
    @correct_slug(Offer, 'offers_join', 'title')
    def post(request, slug, id_):  # pylint: disable=unused-argument
        """View responsible for saving join for particular offer."""
        form = OfferApplyForm(request.POST)
        offer = Offer.objects.get(id=id_)
        if form.is_valid():
            if request.user.is_authenticated():
                user = request.user
            else:
                user = User.objects.filter(
                    email=request.POST.get('email')
                ).exists()

                if user:
                    messages.info(
                        request,
                        "Zaloguj się, aby zapisać się do oferty."
                    )
                    return redirect(
                        '{ANGULAR_ROOT}/login?next={path}'.format(
                            ANGULAR_ROOT=settings.ANGULAR_ROOT,
                            path=request.path,
                        )
                    )

                messages.info(
                    request,
                    "Zarejestruj się, aby zapisać się do oferty."
                )
                return redirect('{ANGULAR_ROOT}/register'.format(
                    ANGULAR_ROOT=settings.ANGULAR_ROOT
                ))

            has_applied = Offer.objects.filter(
                volunteers=user,
                volunteers__offer=id_,
            ).count()
            if has_applied:
                messages.error(
                    request,
                    "Już wyraziłeś chęć uczestnictwa w tej ofercie."
                )
                return redirect('offers_list')

            offer.volunteers.add(user)
            offer.save()
            send_mail(
                request,
                'offer_application',
                [
                    userprofile.user.email
                    for userprofile in offer.organization.userprofiles.all()
                ],
                dict(
                    email=request.POST.get('email'),
                    phone_no=request.POST.get('phone_no'),
                    fullname=request.POST.get('fullname'),
                    comments=request.POST.get('comments'),
                    offer=offer,
                )
            )
            messages.success(
                request,
                "Zgłoszenie chęci uczestnictwa zostało wysłane."
            )
            return redirect(
                '{ANGULAR_ROOT}/offers/{slug}/{id}'.format(
                    ANGULAR_ROOT=settings.ANGULAR_ROOT,
                    slug=slugify(offer.title),
                    id=str(offer.id),
                )
            )
        else:
            errors = "<br />".join(form.errors)
            messages.error(
                request,
                "Formularz zawiera nieprawidłowe dane" + errors
            )
            volunteer_user = UserProfile()
            if request.user.is_authenticated():
                volunteer_user = request.user.userprofile
            return render(
                request,
                'offers/offer_apply.html',
                {
                    'offer': offer,
                    'form': form,
                    'volunteer_user': volunteer_user,
                }
            )
