from buildings.viewsets import CampusViewSet, FloorViewSet
from rest_framework import routers
from users.api import UserViewSet, GroupViewSet

router = routers.DefaultRouter()

router.register(r"users", UserViewSet, base_name="users")
router.register(r"groups", GroupViewSet, base_name="groups")

router.register(r'floor', FloorViewSet, base_name='floors')
router.register(r'campus', CampusViewSet, basename='campus')
