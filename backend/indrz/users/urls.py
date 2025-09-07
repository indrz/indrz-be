from django.urls import re_path, include, path
from rest_framework import routers
from users import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
#
# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


urlpatterns = [
    re_path(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'
    ),
    re_path(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    re_path(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    re_path(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),

]

