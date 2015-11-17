from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('api.views',
    #  ex valid call from to  /api/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2
    #url(r'^directions/(?P<start_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<start_floor>\d+)&(?P<end_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<end_floor>\d+)&(?P<route_type>[0-9])/$', 'create_route', name='directions'),
    url(r'^directions/(?P<start_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<start_floor>[-]?\d+)&(?P<end_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<end_floor>[-]?\d+)&(?P<route_type>[0-9])/$', 'create_route_from_coords', name='root_coords'),
    #url(r'^directions/(?P<start_room_key>\d{5})&(?P<end_room_key>\d{5})&(?P<route_type>[0-9])/$', 'route_room_to_room', name='route-room-to-room'),
    url(r'^directions2/(?P<building_key>building=\d{1,5})&(?P<start_room_key>startid=\d{1,5})&(?P<end_room_key>endid=\d{1,5})(?P<route_type>&type=\d{1,5})?/$',
        'route_room_to_room', name='room-routing'),
    url(r'^directions3/(?P<room_num>\d{5})/$', 'get_room_centroid_node', name='room-center'),
    url(r'^spaces/search/$', 'spaces_list', name='spaces_list'),
    url(r'^directions/(?P<building_name>building=d{1,5})&start={1,6}&destination={1,6}/$', 'route_room_to_room', name='route-space-to-space' )

)
# http://localhost:8000/api/v1/directions/building=1&startid=2&endid=26&type=0
# http://localhost:8000/api/v1/directions/building=1&startid=0E351&endid=1I052

urlpatterns = format_suffix_patterns(urlpatterns)
