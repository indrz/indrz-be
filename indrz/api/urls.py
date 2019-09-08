from django.urls import include, path
from rest_framework import routers
from users.views import UserViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]





# from api import search
# from buildings.views import get_spaces_on_floor, campus_list, campus_buildings_list, campus_buildings_short_list, \
#     space_details, get_campus_info, campus_floor_spaces, campus_locations
# from django.conf.urls import url, include
# from rest_framework.documentation import include_docs_urls
#
# from .search_aau import AauApi
# from .views import get_campus_floors, get_room_center
#
# # SPACES API URLS
# urlpatterns = [
#     # url(r'^spaces/$', 'spaces_list', name='list_all_campuses'),
#     url(r'^getcenter/(?P<big_pk>(\d{3}_\d{2}_[A-Z]{1}[A-Z0-9]{1}[0-9]{2}_\d{6}))/$', get_room_center,
#         name='show_space_details'),
#     url(r'^spaces/(?P<space_id>\d{1,5})/$', space_details, name='show_space_details'),
# ]
#
# # Floors API URLS
# urlpatterns += [
#     url(r'^floors/(?P<floor_id>\d{1,5})/$', get_spaces_on_floor, name='get_spaces_on_floor'),
# ]
#
# # CAMPUS AND BUILDINGS API URLS
# urlpatterns += [
#     url(r'^campus/$', campus_list, name='list_all_campuses'),
#     url(r'^campus/locations/$', campus_locations, name='list_campus_locations'),
#     url(r'^campus/(?P<campus_id>\d{1,5})/floors/$', get_campus_floors, name='campus-floors'),
#     url(r'^campus/(?P<campus_id>\d{1,5})/$', campus_buildings_list, name='campus_building_list'),
#     url(r'^campus/(?P<campus_id>\d{1,5})/shortlist/$', campus_buildings_short_list, name='buildings_list'),
#     url(r'^campus/(?P<campus_id>\d{1,5})/info/$', get_campus_info, name='campus-info'),
#     url(r'^campus/(?P<campus_id>\d{1,5})/floor/(?P<floor_num>\d{1,5})$', campus_floor_spaces, name='campus-floors'),
#     url(r'^campus/(?P<campus_id>\d{1,5})/search/(?P<search_string>.{1,60})', search.search_indrz, name='search_campus'),
#     url(r'^buildings/', include('buildings.urls')),
#
# ]
#
# urlpatterns += [
#
#     url(r'^campus/(?P<campus_id>\d{1,5})/poi/', include('poi_manager.urls')),
#
# ]
#
# # urlpatterns += [
#     # url(r'^$', view_map, name='map_home'),
#     #             url(r'^autocomplete/(?P<search_text>.+)', searchAutoComplete.as_view(), name='search_autocomplete'),
#                 # url(r'^search/(?P<q>.+)', search_any, name='search'),
#                 # url(r'^map/(?P<poicatid>poi-cat-id=\d{1,4})(,\d{1,4})?(,\d{1,4})?(,\d{1,4})?(,\d{1,4})?', view_map, name='map_name'),
#                 # url(r'^map/(?P<map_name>[^/]+)/$', view_map, name='map_name'),
#                 # url(r'^help/$', view_help, name='help'),
#                 # url(r'^aausearch/(?P<q>.+)', AauApi.as_view(), name='aau search')]
#
# # DIRECTIONS API URLS
# urlpatterns += [
#     url(r'^directions/', include('routing.urls')),
#     url(r'^search/.+', AauApi.as_view(), name='aau search')
# ]
#
# urlpatterns += [
#     url(r'^campus/(?P<campus_id>\d{1,5})/poi/', include('poi_manager.urls')),
#     # url(r'^docs/', include_docs_urls(title='Indrz API docs', patterns=doc_urls, public=False)),
# ]
#
# # http://localhost:8000/api/v1/directions/force_mid/?startnode=1385&midnode=1167&endnode=1252
# # http://localhost:8000/api/v1/directions/buildingid=1&startid=307: Orne&endid=311: Mayenne
# # http://localhost:8000/api/v1/directions/buildingid=1&startid=1173&endid=1231
