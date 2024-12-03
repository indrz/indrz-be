import os

from django.conf import settings
from django.urls import re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.search import search_any
from users.views import CustomAuthToken
from .routers import router

##############################################
# Default
##############################################


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
    re_path(r'^api/v1/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/v1/search/(?P<q>.+)/$', search_any, name='search'),
    re_path(r'^api/v1/share/', include(('api.share_urls', 'share_result'), namespace='share_result')),
    re_path(r'^api/v1/directions/', include(('routing.urls', 'directions'), namespace='directions')),
    re_path(r'^api/v1/admin/', admin.site.urls),
    re_path(r'^api/v1/poi/', include(('poi_manager.urls', 'poi'), namespace='poi')),
    re_path(r'^api/v1/health', include('health.urls')),
    re_path(r'^api/v1/', include(router.urls))
]

urlpatterns += [
    re_path(r'^api/v1/api-token-auth/', CustomAuthToken.as_view())
]


urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^translate/', include('rosetta.urls')),
    ]
