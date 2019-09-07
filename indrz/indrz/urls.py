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
from django.contrib.auth import login, logout
from django.urls import path
from django.conf.urls import url

from django.views.generic import TemplateView

admin.site.site_header = 'indrz Administrator'

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('homepage', 'poi_manager', ),  #'maps',
}


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
]


# urlpatterns = [
#     # ...
#     # Route TemplateView to serve Swagger UI template.
#     #   * Provide `extra_context` with view name of `SchemaView`.
#     path('swagger-ui/', TemplateView.as_view(
#         template_name='swagger-ui.html',
#         extra_context={'schema_url':'openapi-schema'}
#     ), name='swagger-ui'),
# ]



urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^translate/', include('rosetta.urls')),
    ]

urlpatterns = [
    # ...
    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns