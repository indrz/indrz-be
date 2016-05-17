from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('api.views',
    #  ex valid call from to  /api/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2
    #url(r'^directions/(?P<start_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<start_floor>\d+)&(?P<end_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<end_floor>\d+)&(?P<route_type>[0-9])/$', 'create_route', name='directions'),

    # url(r'^spaces/search/(?P<search_term>[a-zA-Z0-9]{2,5})/$', 'autocomplete_list', name='spaces_list'),
    url(r'^spaces/search/$', 'autocomplete_list', name='spaces_list'),
    url(r'^buildings/$', 'building_list', name='list_buildings'),
    url(r'^building/list/$', 'building_short_list', name='building_short_list'),
    url(r'^building/campus/(?P<pk_campus>[0-9]+)/$', 'list_buildings_on_campus', name='building_on_campus_list'),
    url(r'^buildings/(?P<pk>[0-9]+)/$', 'building_detail', name='building_details'),
    url(r'^buildings/spaces/(?P<building_id>\d{1,5})/(?P<floor_id>\d{1,5})/$', 'building_spaces_list', name='building_spaces_list'),
    url(r'^buildings/space/(?P<space_id>\d{1,5})/$', 'get_floor_space_id', name='get_space_info'),
    url(r'^buildings/floor/(?P<building_id>\d{1,5})/$', 'building_floors_list', name='get_floor_ids'),

    url(r'^building/(?P<building_id>\d{1,5})/externid/(?P<external_room_id>.+)/$', 'get_external_id', name='get_external_ids'),
    url(r'^building/(?P<building_id>\d{1,5})/(?P<space_name>.+)/$', 'get_space_by_name', name='get_space_by_name'),
    #url(r'^directions/(?P<building_name>building=d{1,5})&start={1,6}&destination={1,6}/$', 'route_room_to_room', name='route-space-to-space' )

)

urlpatterns += patterns('routing.views',
    url(r'^directions/(?P<start_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<start_floor>[-]?\d+)&(?P<end_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<end_floor>[-]?\d+)&(?P<route_type>[0-9])/$',
        'create_route_from_coords', name='root_coords'),
    #url(r'^directions/(?P<start_room_key>\d{5})&(?P<end_room_key>\d{5})&(?P<route_type>[0-9])/$', 'route_room_to_room', name='route-room-to-room'),
    url(r'^directions/(?P<building_id>buildingid=\d{1,5})&(?P<start_room_id>startid=\d{1,5})&(?P<end_room_id>endid=\d{1,5})(?P<route_type>&type=\d{1,5})?/$',
        'create_route_from_id', name='routing-from-id'),
    url(r'^directions/(?P<building_id>buildingid=\d{1,5})&(?P<start_term>startid=.+)&(?P<end_term>endid=.+)(?P<route_type>&type=\d{1,5})?/$',
        'create_route_from_search', name='routing-from-search'),
    url(r'^directions/force_mid/', 'force_route_mid_point', name='force-route-midpoint')

                        )
# http://localhost:8000/api/v1/directions/force_mid/?startnode=1385&midnode=1167&endnode=1252
# http://localhost:8000/api/v1/directions/buildingid=1&startid=307: Orne&endid=311: Mayenne
# http://localhost:8000/api/v1/directions/buildingid=1&startid=1173&endid=1231

urlpatterns = format_suffix_patterns(urlpatterns)
