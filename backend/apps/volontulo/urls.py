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
from apps.volontulo.views import pages as pages_views


router = DefaultRouter()
router.register(r'offers', api_views.OfferViewSet, base_name='offer')
router.register(r'organizations', api_views.OrganizationViewSet)


handler404 = 'apps.volontulo.views.page_not_found'
handler500 = 'apps.volontulo.views.server_error'

urlpatterns = [
    url(r'^$', views.homepage_redirect, name='homepage_redirect'),

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

    # homepage:
    url(r'^o$', views.homepage, name='homepage'),

    # login and loggged user space:
    url(r'^o/login$', auth_views.login, name='login'),
    url(r'^o/logout$', auth_views.logout, name='logout'),
    url(r'^o/register$', auth_views.Register.as_view(), name='register'),
    url(
        r'^o/activate/(?P<uuid>[-0-9A-Za-z]+)$',
        auth_views.activate,
        name='activate'
    ),
    url(
        r'^o/password-reset$',
        auth_views.password_reset,
        name='password_reset'
    ),
    url(
        r'^o/password-reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'
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
        r'^o/offers/(?P<slug>[\w-]+)/(?P<id_>[0-9]+)$',
        offers_views.OffersView.as_view(),
        name='offers_view'
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
        r'^o/organizations$',
        orgs_views.organizations_list,
        name='organizations_list'
    ),
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
    # organizations/<slug>/<id>/contact


    # pages:
    url(
        r'^o/pages$',
        pages_views.PageList.as_view(),
        name='pages_list'
    ),
    url(
        r'^o/pages/create$',
        pages_views.PageCreate.as_view(),
        name='pages_create'
    ),
    url(
        r'^o/pages/(?P<pk>[0-9]+)/edit',
        pages_views.PageEdit.as_view(),
        name='pages_edit'
    ),
    url(
        r'^o/pages/(?P<pk>[0-9]+)/delete',
        pages_views.PageDelete.as_view(),
        name='pages_delete'
    ),
    url(
        r'^o/(?P<slug>[-\w]+),(?P<pk>[0-9]+).html$',
        pages_views.PageDetails.as_view(),
        name='pages_detail'
    ),

    # others:
    url(
        r'^o/o-nas$',
        views.static_pages,
        kwargs={'template_name': 'about-us'},
        name='about-us'
    ),
    url(
        r'^o/office$',
        views.static_pages,
        kwargs={'template_name': 'office'},
        name='office'
    ),
    url(
        r'^o/pages/(?P<template_name>[\w-]+)$',
        views.static_pages,
        name='static_page'
    ),
    url(
        r'^o/contact$',
        views.contact_form,
        name='contact_form'
    ),
    url(
        r'^o/newsletter$',
        views.newsletter_signup,
        name='newsletter_signup'
    ),
]
