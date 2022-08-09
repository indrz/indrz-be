from rest_framework import routers
from users.api import UserViewSet, GroupViewSet
from buildings.api import BuildingsViewSet, CampusViewSet, FloorViewSet

router = routers.DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"groups", GroupViewSet, basename="groups")
router.register(r'floor', FloorViewSet, basename='floors')
router.register(r'campus', CampusViewSet, basename='campus')
router.register(r'buildings', BuildingsViewSet, basename='buildings')