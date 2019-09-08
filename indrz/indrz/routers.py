from rest_framework import routers
from django.urls import include, path

router = routers.DefaultRouter()

# Users & Roles
from users.views import UserViewSet

router.register(r"users", UserViewSet, base_name="users")
