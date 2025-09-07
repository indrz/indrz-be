# myproject/urls.py
from django.urls import path, re_path
from health.views import VersionAPIView, health_check

urlpatterns = [
    # JSON API response
    re_path(r'^$', health_check, name='health_check'),
    path('version/', VersionAPIView.as_view(), name='api-version'),
]