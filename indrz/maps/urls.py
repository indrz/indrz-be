from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

# all urls begin with http://localhost:8000/maps/
urlpatterns = patterns('maps.views',
    #  ex valid call from to  /api/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2
    # url(r'^(?P<map_name>[0-9a-zA-Z_-]+)/$', 'route_map', name='map_name'),
    url(r'^$', 'map_socgen_nantes', name='socgen-nantes'),
    url(r'^(?P<map_name>.+)/$', 'route_map', name='map_name'),
    url(r'^socgen-nantes/$', 'map_socgen_nantes', name='socgen-nantes'),
    url(r'^space/(?P<space_id>\d{1,5})(?P<zoom_level>&zoom=\d{1,2})?/$', 'zoom_space', name='zoom-space'),
    url(r'^campus/(?P<campus_id>\d{1,5})(?P<zoom_level>&zoom=\d{1,2})?/$', 'zoom_campus', name='zoom-campus'),
    url(r'^building/(?P<building_id>\d{1,5})(?P<zoom_level>&zoom=\d{1,2})?/$', 'zoom_building', name='zoom-building'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
