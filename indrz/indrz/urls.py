"""indrz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import javascript_catalog
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

from bookway.routers import router
from rest_framework.documentation import include_docs_urls

from kiosk.views import homepage_kiosk


admin.site.site_header = 'indrz Administrator'

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('homepage', 'poi_manager', ),  #'maps',
}


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', 'maps.views.view_map'),  # homepage start page url


    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),




    # url(r'^map/', include('maps.urls')),

    #url(r'^wu/', include('homepage.urls')),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict,
        name='javascript-catalog'),



]

urlpatterns += i18n_patterns(
    url(r'^', include('homepage.urls')),
    url(r'^bookway/', include('bookway.urls')),
    url(r'^indrz/api/v1/', include('api.urls')),
    url(r'^indrz/kiosk/', include('kiosk.urls')),
    # url(r'^indrz/kiosk/$', homepage_kiosk, name="kiosk-home"),
)


urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^rosetta/', include('rosetta.urls')),
    ]

if 'rest_framework_swagger' in settings.INSTALLED_APPS:
    schema_view = get_swagger_view(title='INDRZ API')
    urlpatterns += [
        url(r'^indrz/api/v1/docs/', schema_view),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns