# -*- coding: utf-8 -*-

"""
.. module:: urls
"""

from django.conf.urls import include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from apps.volontulo import views
from apps.volontulo.views import api as api_views
from apps.volontulo.views import auth as auth_views
from apps.volontulo.views import offers as offers_views

router = DefaultRouter()
router.register(r'offers', api_views.OfferViewSet, base_name='offer')
router.register(r'organizations', api_views.OrganizationViewSet)


handler404 = 'apps.volontulo.views.page_not_found'
handler500 = 'apps.volontulo.views.server_error'

urlpatterns = [
    # api:
    url(r'^api/', include(router.urls)),
    url(
        r'^api/login/$',
        api_views.login_view,
        name='api_login'
    ),
    url(
        r'^api/logout/$',
        api_views.logout_view,
        name='api_logout'
    ),
    url(
        r'^api/current-user/$',
        api_views.CurrentUser.as_view(),
        name='current_user'
    ),
    url(
        r'^api/password-reset/$',
        api_views.password_reset,
        name='password_reset'
    ),
    url(
        r'^api/password-reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$',
        api_views.password_reset_confirm,
        name='password_reset_confirm'
    ),
    url(
        r'^api/password-change/',
        api_views.PasswordChangeView.as_view(),
        name='password_change',
    ),
    url(r'^api/messages/$', api_views.messages_view, name='messages'),
    url(r'^api/contact/$', api_views.Contact.as_view(), name='contact'),
    url(
        r'^api/register/$',
        api_views.register_view,
        name='register'
    ),
    url(
        r'^api/activate/(?P<uuid>[-0-9A-Za-z]+)/$',
        api_views.activate_view,
        name='activate'
    ),


    # login and loggged user space:
    url(r'^o/logout$', auth_views.logout, name='logout'),
    url(r'^o/me$', views.logged_user_profile, name='logged_user_profile'),
    # me/edit
    # me/settings

    # offers' namesapce:
    url(r'^o/offers$', offers_views.OffersList.as_view(), name='offers_list'),
    url(
        r'^o/offers/accept/(?P<pk>[0-9]+)$',
        offers_views.OffersAccept.as_view(),
        name='offers_accept'
    ),
    url(
        r'^o/offers/reorder/(?P<id_>[0-9]+)?$',
        offers_views.OffersReorder.as_view(),
        name='offers_reorder'
    ),
    url(
        r'^o/offers/(?P<slug>[\w-]+)/(?P<id_>[0-9]+)/join$',
        offers_views.OffersJoin.as_view(),
        name='offers_join'
    ),
    # offers/filter

    # users' namesapce:
    # users
    # users/filter
    # users/slug-id
    # users/slug-id/contact

    # organizations/filter
]
