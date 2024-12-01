from django.conf.urls import url, re_path
from routing.views import NearestPoi, RoutePoiToXyzV0, route_space_id_and_poi_id
from routing.views import create_route_from_coords, create_route_from_id, create_route_from_search
from routing.views import (force_route_mid_point, route_to_nearest_poi, RoutePoiToPoi, RouteSpaceToXyz,
                           RouteXyzToXyz, RoutePoiToXyz )

urlpatterns = [
    url(
        r'(?P<start_xy>startxy=[-]?\d+\.?\d+,\d+\.\d+)&(?P<floor>floor=[-]?\d+)(?P<poi_cat_id>&poiCatId=\d{1,7})(?P<reversed>&reversed=(true|false))?(?P<route_type>&type=\d{1,5})?/$',
        route_to_nearest_poi, name='routing-from-poi'),
    url(
        r'(?P<start_poi_id>poi-id=\d{1,7})&(?P<end_xyz>xyz=[-]?\d+\.?\d+,\d+\.\d+)&(?P<z_floor>floor=[-]?\d+)&?(?P<reversed_dir>reversed=(true|false))?(?P<route_type>&type=\d{1,5})?/$',
        RoutePoiToXyzV0.as_view(), name='route_poi_to_xyz'),
    url(
        r'(?P<start_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<start_floor>[-]?\d+)&(?P<end_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<end_floor>[-]?\d+)&(?P<route_type>[0-9])(?P<reverse_route>&reversed=(true|false))?',
        create_route_from_coords, name='root_coords'),
    # url(r'^directions/(?P<start_room_key>\d{5})&(?P<end_room_key>\d{5})&(?P<route_type>[0-9])/$', 'route_room_to_room', name='route-room-to-room'),
    url(
        r'(?P<start_room_id>startid=\d{1,10})&(?P<end_room_id>endid=\d{1,7})(?P<route_type>&type=\d{1,5})?(?P<front_office_id>&foid=\d{1,7})?/$',
        create_route_from_id, name='routing-from-id'),
    url(
        r'(?P<start_poi_id>start-poi-id=\d{1,7})&(?P<end_poi_id>end-poi-id=\d{1,7})?(?P<route_type>&type=\d{1,5})?/$',
        RoutePoiToPoi.as_view(), name='route-poi-to-poi'),
    url(
        r'(?P<space_id>space-id=\d{1,7})&(?P<xyz>xyz=[-]?\d+\.?\d+,[-]?\d+\.\d+,[-]?\d+\.\d{1})?(?P<reversed>&reversed=(true|false))?(?P<route_type>&type=\d{1,5})?/$',
        RouteSpaceToXyz.as_view(), name='route-space-to-xyz'),
    re_path(
        r'(?P<start_xyz>start_xyz=[-]?\d+\.?\d+,[-]?\d+\.\d+,[-]?\d+\.\d{1})&(?P<end_xyz>end_xyz=[-]?\d+\.?\d+,[-]?\d+\.\d+,[-]?\d+\.\d{1})?(?P<route_type>&type=\d{1,5})?/$',
        RouteXyzToXyz.as_view(), name='route-xyz-to-xyz'),
    re_path(
        r'(?P<start_poi_id>poi=\d{1,10})&(?P<end_xyz>xyz=[-]?\d+\.?\d+,[-]?\d+\.\d+,[-]?\d+\.\d{1})(&?(?P<reversed_dir>reversed=(true|false)))?(&?(?P<route_type>type=\d{1,5}))?/$',
        RoutePoiToXyz.as_view(), name='route_poi_to_xyz'),
    url(
        r'(?P<start_term>startstr=.+)&(?P<end_term>endstr=.+)&(?P<route_type>type=\d{1,7})/$',
        create_route_from_search, name='routing-from-search'),

    url(r'force_mid/', force_route_mid_point, name='force-route-midpoint'),
    url(
        r'near/(?P<coordinates>coords=[-]?\d+\.?\d+,\d+\.\d+)&(?P<floor>floor=[-]?\d+)(?P<poi_cat_id>&poiCatId=\d{1,5})/$',
        NearestPoi.as_view(), name='nearest-poi'),
    url(
        r'(?P<space_id>space-id=\d{1,7})&(?P<poi_id>poi-id=\d{1,7})(?P<route_type>&type=\d{1,5})?/$',
        route_space_id_and_poi_id, name='route-space-to-poi'),

]
