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
from apps.volontulo.views import organizations as orgs_views

router = DefaultRouter()
router.register(r'offers', api_views.OfferViewSet, base_name='offer')
router.register(r'organizations', api_views.OrganizationViewSet)


handler404 = 'apps.volontulo.views.page_not_found'
handler500 = 'apps.volontulo.views.server_error'

urlpatterns = [
    # api:
    url(r'^api/', include(router.urls)),
    url(
        r'^api/login',
        api_views.login_view,
        name='api_login'
    ),
    url(
        r'^api/logout',
        api_views.logout_view,
        name='api_logout'
    ),
    url(
        r'^api/current-user',
        api_views.current_user,
        name='current_user'
    ),
    url(
        r'^api/password-reset$',
        api_views.password_reset,
        name='password_reset'
    ),
    url(
        r'^api/password-reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)$',
        api_views.password_reset_confirm,
        name='password_reset_confirm'
    ),
    url(r'^api/messages/$', api_views.messages_view, name='messages'),

    # login and loggged user space:
    url(r'^o/logout$', auth_views.logout, name='logout'),
    url(r'^o/register$', auth_views.Register.as_view(), name='register'),
    url(
        r'^o/activate/(?P<uuid>[-0-9A-Za-z]+)$',
        auth_views.activate,
        name='activate'
    ),
    url(r'^o/me$', views.logged_user_profile, name='logged_user_profile'),
    # me/edit
    # me/settings

    # offers' namesapce:
    url(r'^o/offers$', offers_views.OffersList.as_view(), name='offers_list'),
    url(
        r'^o/offers/delete/(?P<pk>[0-9]+)$',
        offers_views.OffersDelete.as_view(),
        name='offers_delete'
    ),
    url(
        r'^o/offers/accept/(?P<pk>[0-9]+)$',
        offers_views.OffersAccept.as_view(),
        name='offers_accept'
    ),
    url(
        r'^o/offers/create$',
        offers_views.OffersCreate.as_view(),
        name='offers_create'
    ),
    url(
        r'^o/offers/reorder/(?P<id_>[0-9]+)?$',
        offers_views.OffersReorder.as_view(),
        name='offers_reorder'
    ),
    url(
        r'^o/offers/archived$',
        offers_views.OffersArchived.as_view(),
        name='offers_archived'
    ),
    url(
        r'^o/offers/(?P<slug>[\w-]+)/(?P<id_>[0-9]+)/edit$',
        offers_views.OffersEdit.as_view(),
        name='offers_edit'
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

    # organizations' namespace:
    url(
        r'^o/organizations/create$',
        orgs_views.OrganizationsCreate.as_view(),
        name='organizations_create',
    ),
    url(
        r'^o/organizations/(?P<slug>[\w-]+)/(?P<id_>[0-9]+)$',
        orgs_views.organization_view,
        name='organization_view'
    ),
    url(
        r'^o/organizations/(?P<slug>[\w-]+)/(?P<id_>[0-9]+)/edit$',
        orgs_views.organization_form,
        name='organization_form'
    ),
    # organizations/filter

    url(
        r'^o/contact$',
        views.contact_form,
        name='contact_form'
    ),
]
