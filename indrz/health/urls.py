# health/urls.py
from django.urls import re_path
from . import views

app_name = 'health'

urlpatterns = [
    re_path('/', views.health_check, name='health_check'),
]

# Add to your main urls.py:
# path('', include('health.urls')),