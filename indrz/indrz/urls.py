from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from .routers import router

##############################################
# Default
##############################################

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^translate/', include('rosetta.urls')),
    ]


##############################################
# Static and media files in debug mode
##############################################

# if settings.DEBUG:
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
#     def mediafiles_urlpatterns(prefix):
#         """
#         Method for serve media files with runserver.
#         """
#         import re
#         from django.views.static import serve
#
#         return [
#             url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), serve,
#                 {'document_root': settings.MEDIA_ROOT})
#         ]
#
#     # Hardcoded only for development server
#     urlpatterns += staticfiles_urlpatterns(prefix="/static/")
#     urlpatterns += mediafiles_urlpatterns(prefix="/media/")


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns