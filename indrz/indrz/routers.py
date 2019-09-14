from rest_framework import routers
from django.urls import include, path

from buildings.views import CampusViewSet
from users.views import UserViewSet

router = routers.DefaultRouter()


router.register(r"users", UserViewSet, base_name="users")
router.register(r'campus', CampusViewSet)


# # CAMPUS AND BUILDINGS API URLS
# urlpatterns += [
#     path(r'^campus/$', campus_list, name='list_all_campuses'),
#     path(r'^campus/locations/$', campus_locations, name='list_campus_locations'),
#     path(r'^campus/(?P<campus_id>\d{1,5})/floors/$', get_campus_floors, name='campus-floors'),
#     path(r'^campus/(?P<campus_id>\d{1,5})/$', campus_buildings_list, name='campus_building_list'),
#     path(r'^campus/(?P<campus_id>\d{1,5})/shortlist/$', campus_buildings_short_list, name='buildings_list'),
#     path(r'^campus/(?P<campus_id>\d{1,5})/info/$', get_campus_info, name='campus-info'),
#     path(r'^campus/(?P<campus_id>\d{1,5})/floor/(?P<floor_num>\d{1,5})$', campus_floor_spaces, name='campus-floors'),
#     path(r'^campus/(?P<campus_id>\d{1,5})/search/(?P<search_string>.{1,60})', search.search_indrz, name='search_campus'),
#     path(r'^buildings/', include('buildings.urls')),
#
# ]
