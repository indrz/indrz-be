import json

from django.shortcuts import render
from django.utils import translation
from django.conf import settings

from buildings.models import Campus

from geojson import Feature

from poi_manager.models import PoiCategory
from django.views.decorators.clickjacking import xframe_options_exempt

from django.conf import settings


@xframe_options_exempt
def view_map(request, *args, **kwargs):
    context = {}
    if request.method == 'GET':
        map_name = kwargs.pop('map_name', None)
        building_id, = request.GET.get('buildingid', 1),
        campus_id = request.GET.get('campus', 1),
        space_id, = request.GET.get('spaceid', 0),
        zoom_level, = request.GET.get('zlevel', 17),
        route_from, = request.GET.get('startstr', ''),
        route_to, = request.GET.get('endstr', ''),
        route_to_spaceid, = request.GET.get('end-spaceid', 0),
        route_from_spaceid, = request.GET.get('start-spaceid', 0),
        route_from_xyz, = request.GET.get('start-xyz', ''),
        route_to_xyz, = request.GET.get('end-xyz', ''),
        route_from_poi_id, = request.GET.get('start-poiid', 0),
        route_to_poi_id, = request.GET.get('end-poiid', 0),
        route_type, = request.GET.get('type','0'),
        centerx, = request.GET.get('centerx', 0),
        centery, = request.GET.get('centery', 0),
        floor_num, = request.GET.get('floor', 1),
        poi_name, = request.GET.get('poi-name', ''),
        poi_cat_name, = request.GET.get('poi', 'none'),
        poi_cat_id, = request.GET.get('poi-cat-id', 'noid'),
        search_text, = request.GET.get('q', ''),
        poi_id, = request.GET.get('poi-id', 'none'),
        poi_start_id, = request.GET.get('start-poi-id', -1),
        poi_end_id, = request.GET.get('end-poi-id', -1),
        share_xy = request.GET.get('search', ''),
        hide_left_menu = request.GET.get('hide-left', 'false')
        hide_top = request.GET.get('hide-top', 'false')
        hide_footer = request.GET.get('hide-footer', 'false')
        floor_num = int(floor_num)
        library_key = request.GET.get('key', 'nokey')

        req_locale = translation.get_language_from_request(request, check_path=True)

        host_url = settings.LOCALHOST_URL

        newcats = []
        poi_cats = poi_cat_id.split(",")

        if poi_cats != ['noid']:

            for x in poi_cats:
                newcats.append(int(x))

        # TODO update start floor number variables to reflect floor numbers
        # we use index list of floor numbers and that does not reflect negative
        # floor numbers such as -1, -2
        # uncomment these if campus has underground floor like wu  -1, -2
        # reason is that the index starts at 0
        # if floor_num == 0:
        #     floor_num = floor_num + 1
        # else:
        #     floor_num = floor_num + 1

        if isinstance(centerx, str):
            if ',' in centerx:
                centerx = float(centerx.replace(',', '.'))
                centery = float(centery.replace(',', '.'))


        context.update({
            'map_name': map_name,
            'building_id': building_id,
            'campus_id': campus_id,
            'space_id': int(space_id),
            'zoom_level': zoom_level,
            'route_from': route_from,
            'route_to': route_to,
            'route_from_spaceid': int(route_from_spaceid),
            'route_to_spaceid': int(route_to_spaceid),
            'route_from_xyz': route_from_xyz,
            'route_to_xyz': route_to_xyz,
            'route_from_poi_id': route_from_poi_id,
            'route_to_poi_id': route_to_poi_id,
            'route_type': route_type,
            'centerx': centerx,
            'centery': centery,
            'floor_num': int(floor_num),
            'poi_name': poi_name,
            'poi_cat_name': poi_cat_name,
            'poi_cat_id': json.dumps(newcats),
            'search_text': search_text,
            'poi_id': poi_id,
            'poi_start_id': int(poi_start_id),
            'poi_end_id': int(poi_end_id),
            'share_xy': share_xy,
            'hide_top': hide_top,
            'hide_left': hide_left_menu,
            'hide_footer': hide_footer,
            'library_key': library_key,
            'req_locale': req_locale,
            'host_url': host_url,
            'nodes': PoiCategory.objects.filter(enabled=True),
            'campusLocations': Campus.objects.all(),
            'indrz_token': settings.INDRZ_API_TOKEN,
        })

    return render(request, context=context, template_name='index.html')
