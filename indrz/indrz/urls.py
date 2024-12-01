from api.search import search_any
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from users.views import CustomAuthToken
import os
from .routers import router

admin.site.site_header = 'INDRZ Manager'

schema_view = get_schema_view(
   openapi.Info(
      title="INDRZ API",
      default_version='v1',
      description="Indrz mapping apis",
      terms_of_service="https://www.indrz.com",
      contact=openapi.Contact(email="sales@gomogi.com"),
      license=openapi.License(name="MIT License"),
   ),
   url=os.getenv('SWAGGER_URL'),
   public=False,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api/v1/api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),
    url(r'^api/v1/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api/v1/search/(?P<q>.+)', search_any, name='search'),
    url(r'^api/v1/share/', include(('api.share_urls', 'share_result'), namespace='share_result')),
    url(r'^api/v1/directions/', include(('routing.urls', 'directions'), namespace='directions')),
    url(r'^api/v1/admin/', admin.site.urls),
    url(r'^api/v1/poi/', include(('poi_manager.urls', 'poi'), namespace='poi')),
    url(r'^api/v1/', include(router.urls))
]

urlpatterns += [
    url(r'^api/v1/api-token-auth/', CustomAuthToken.as_view())
]

urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^translate/', include('rosetta.urls')),
    ]


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
            url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), serve,
                {'document_root': settings.MEDIA_ROOT})
        ]

    # Hardcoded only for development server
    urlpatterns += staticfiles_urlpatterns(prefix="/static/")
    urlpatterns += mediafiles_urlpatterns(prefix="/media/")
