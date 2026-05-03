import os

from django.conf import settings
from django.urls import re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions

from api.search import search_any
from users.views import CustomAuthToken
from .routers import router
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView, SpectacularAPIView

##############################################
# Default
##############################################


admin.site.site_header = 'INDRZ Manager'



urlpatterns = [
    path('api/v1/api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),
    re_path(r'^api/v1/schema/$', SpectacularAPIView.as_view(), name='schema'),
    re_path(r'^api/v1/docs/', SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    re_path(r'^api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    re_path(r'^api/v1/search/(?P<q>.+)/$', search_any, name='search'),
    re_path(r'^api/v1/share/', include(('api.share_urls', 'share_result'), namespace='share_result')),
    re_path(r'^api/v1/directions/', include(('routing.urls', 'directions'), namespace='directions')),
    re_path(r'^api/v1/admin/', admin.site.urls),
    re_path(r'^api/v1/poi/', include(('poi_manager.urls', 'poi'), namespace='poi')),
    re_path(r'^api/v1/bookway/', include(('bookway.urls', 'bookway'), namespace='bookway')),
    re_path(r'^api/v1/health', include('health.urls')),
    re_path(r'^api/v1/', include(router.urls)),
    re_path(r'^api/health/', include(('health.urls', 'health'), namespace='health')),
]

urlpatterns += [
    re_path(r'^api/v1/api-token-auth/', CustomAuthToken.as_view())
]


urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


##############################################
# Static and media files in debug mode
##############################################

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    def mediafiles_urlpatterns(prefix):
        """
        Method for serve media files with runserver.
        """
        import re
        from django.views.static import serve

        return [
            re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), serve,
                {'document_root': settings.MEDIA_ROOT})
        ]

    # Hardcoded only for development server
    urlpatterns += staticfiles_urlpatterns(prefix="/static/")
    urlpatterns += mediafiles_urlpatterns(prefix="/media/")
