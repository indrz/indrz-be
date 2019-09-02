from django.conf.urls import url, include
# from django.conf import settings
# from routing.views import create_route_from_coords, create_route_from_id, create_route_from_search, \
#     force_route_mid_point
from rest_framework.documentation import include_docs_urls

from buildings.views import get_spaces_on_floor, campus_list, campus_buildings_list, campus_buildings_short_list, \
    space_details, get_campus_info, campus_floor_spaces, campus_locations
from homepage.search_aau import search_any, AauApi

from homepage.views import get_campus_floors
from api import search

from homepage.views import get_room_center

# SPACES API URLS
urlpatterns = [
    # url(r'^spaces/$', 'spaces_list', name='list_all_campuses'),
    url(r'^getcenter/(?P<big_pk>(\d{3}_\d{2}_[A-Z]{1}[A-Z0-9]{1}[0-9]{2}_\d{6}))/$', get_room_center,
        name='show_space_details'),
    url(r'^spaces/(?P<space_id>\d{1,5})/$', space_details, name='show_space_details'),
]

# Floors API URLS
urlpatterns += [
    url(r'^floors/(?P<floor_id>\d{1,5})/$', get_spaces_on_floor, name='get_spaces_on_floor'),
    # url(r'^spaces/(?P<space_name>.+)/$', 'get_space_by_name', name='get_space_by_name'),
]

# CAMPUS AND BUILDINGS API URLS
urlpatterns += [
    url(r'^campus/$', campus_list, name='list_all_campuses'),
    url(r'^campus/locations/$', campus_locations, name='list_campus_locations'),
    url(r'^campus/(?P<campus_id>\d{1,5})/floors/$', get_campus_floors, name='campus-floors'),
    url(r'^campus/(?P<campus_id>\d{1,5})/$', campus_buildings_list, name='campus_building_list'),
    url(r'^campus/(?P<campus_id>\d{1,5})/shortlist/$', campus_buildings_short_list, name='buildings_list'),
    url(r'^campus/(?P<campus_id>\d{1,5})/info/$', get_campus_info, name='campus-info'),
    url(r'^campus/(?P<campus_id>\d{1,5})/floor/(?P<floor_num>\d{1,5})$', campus_floor_spaces, name='campus-floors'),
    url(r'^campus/(?P<campus_id>\d{1,5})/search/(?P<search_string>.{1,60})', search.search_indrz, name='search_campus'),
    url(r'^buildings/', include('buildings.urls')),

]

urlpatterns += [

    url(r'^campus/(?P<campus_id>\d{1,5})/poi/', include('poi_manager.urls')),

]

urlpatterns += [

    url(r'^library/', include('bookway.urls')),

]

urlpatterns += [

    url(r'^kiosk/', include('kiosk.urls')),

]

# DIRECTIONS API URLS
urlpatterns += [
    url(r'^directions/', include('routing.urls')),
url(r'^search/.+', AauApi.as_view(), name='aau search')
]

doc_urls = [url(r'^indrz/api/v1/', include('api.urls'), name="api urls"),
   ]


urlpatterns += [
    url(r'^campus/(?P<campus_id>\d{1,5})/poi/', include('poi_manager.urls')),
    url(r'^docs/', include_docs_urls(title='Indrz API docs', patterns=doc_urls, public=False)),
]

# http://localhost:8000/api/v1/directions/force_mid/?startnode=1385&midnode=1167&endnode=1252
# http://localhost:8000/api/v1/directions/buildingid=1&startid=307: Orne&endid=311: Mayenne
# http://localhost:8000/api/v1/directions/buildingid=1&startid=1173&endid=1231
