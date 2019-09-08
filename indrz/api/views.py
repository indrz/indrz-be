#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json

from django.shortcuts import render
from django.utils import translation

from buildings.models import BuildingFloorSpace, Campus

from buildings.serializers import CampusFloorSerializer
from poi_manager.models import PoiCategory
from django.views.decorators.clickjacking import xframe_options_exempt

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from buildings.models import BuildingFloor
from buildings.serializers import FloorListSerializer


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

    return render(request, context=context, template_name='map.html')







def view_help(request, *args, **kwargs):
    context = {}
    if request.method == 'GET':
        return render(request, template_name='hilfe.html')


icon_map = [{"name": "icon-h", "description": "exit"},
            {"name": "icon-g", "description": "stairs-up"},
            {"name": "icon-i", "description": "ramp-up"},
            {"name": "icon-l", "description": "baby"},
            {"name": "icon-n", "description": "fountain"},
            {"name": "icon-t", "description": "plus"},
            {"name": "icon-o", "description": "people"},
            {"name": "icon-p", "description": "info-library"},
            {"name": "icon-q", "description": "sit-workstation"},
            {"name": "icon-r", "description": "stand-workstation"},
            {"name": "icon-s", "description": "hanger"},
            {"name": "icon-u", "description": "no-mobiles"},
            {"name": "icon-v", "description": "phone-booth"},
            {"name": "icon-y", "description": "security-camera"},
            {"name": "icon-B", "description": "no-dogs"},
            {"name": "icon-C", "description": "no-sound"},
            {"name": "icon-D", "description": "no-fire"},
            {"name": "icon-E", "description": "no-skateboarding"},
            {"name": "icon-F", "description": "parking"},
            {"name": "icon-G", "description": "parking-payment"},
            {"name": "icon-H", "description": "motorcycle"},
            {"name": "icon-I", "description": "delivery"},
            {"name": "icon-J", "description": "bike-parking"},
            {"name": "icon-L", "description": "basketball"},
            {"name": "icon-M", "description": "pingpong"},
            {"name": "icon-N", "description": "cafe"},
            {"name": "icon-O", "description": "food"},
            {"name": "icon-Q", "description": "sitting-area"},
            {"name": "icon-S", "description": "shopping-cart"},
            {"name": "icon-T", "description": "smoking"},
            {"name": "icon-U", "description": "printer"},
            {"name": "icon-V", "description": "print-station"},
            {"name": "icon-W", "description": "scanner"},
            {"name": "icon-Y", "description": "self-checkout"},
            {"name": "icon-Z", "description": "quiet-area"},
            {"name": "icon-zero", "description": "info-point"},
            {"name": "icon-one", "description": "triangle"},
            {"name": "icon-two", "description": "arrow-up"},
            {"name": "icon-R", "description": "shopping-cart-empty"},
            {"name": "icon-X", "description": "books"},
            {"name": "icon-a", "description": "elevator-a"},
            {"name": "icon-b", "description": "elevator-b"},
            {"name": "icon-c", "description": "elevator-c"},
            {"name": "icon-d", "description": "elevator"},
            {"name": "icon-x", "description": "info"},
            {"name": "icon-K", "description": "basketball"},
            {"name": "icon-w", "description": "women-wc"},
            {"name": "icon-m", "description": "men-wc"},
            {"name": "icon-j", "description": "wc"},
            {"name": "icon-k", "description": "wheelchair"},
            {"name": "icon-z", "description": "locker"},
            {"name": "icon-P", "description": "family"},
            {"name": "icon-f", "description": "stairs-arrow-up"},
            {"name": "icon-A", "description": "no-smoking"},
            {"name": "icon-e", "description": "stairs-arrow-down"},
            {"name": "icon-three", "description": "defi"},
            {"name": "icon-four", "description": "info-triangle"},
            {"name": "icon-five", "description": "baby-buggy"},
            {"name": "icon-Agrave", "description": "p1"},
            {"name": "icon-Aacute", "description": "p2"},
            {"name": "icon-Acircumflex", "description": "p3"},
            {"name": "icon-Atilde", "description": "p4"},
            {"name": "icon-six", "description": "meeting-point"},
            {"name": "icon-agrave", "description": "elevator-d"},
            {"name": "icon-aacute", "description": "elevator-e"},
            {"name": "icon-seven", "description": "ramp-down"},
            {"name": "icon-eight", "description": "bicycle"},
            {"name": "icon-nine", "description": "bike-covered"},
            {"name": "icon-colon", "description": "front-office"}]


@api_view(['GET'])
def get_campus_floors(request, campus_id, format=None):
    """
    Get a list of floors on campus
    """
    if request.method == 'GET':
        # floor_list = BuildingFloor.objects.order_by('floor_num').distinct('floor_num')
        floor_list = BuildingFloor.objects.order_by('floor_num').distinct('floor_num')
        data = FloorListSerializer(floor_list, many=True)

        return Response(data.data)


@api_view(['GET'])
def get_room_center(request, big_pk, format=None):
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    ip_addr = get_client_ip(request)
    # print('this is my IP : ' + ip_addr)

    if ip_addr.startswith('127.0.'):
        # if q.keys().index('searchString') < 0:
        #     raise Exception("Couldn't find AKS in parameter q")

        # searchString = q['searchString'].upper()
        searchString = big_pk.upper()

        if re.match('(\d{3}_\d{2}_[A-Z]{1}[A-Z0-9]{1}[0-9]{2}_\d{6})', searchString):
            re_is_match = "yes"
        else:
            raise Exception("input search string does not match AKS form zb 001_10_OG05_111200 or 001_10_U101_111900 ")

        # dont allow empty searchString, too short searchString or too long searchString (50 characters is way too much
        #  and probably a sql attack so we prevent it here aswell
        if searchString == "" or len(searchString) < 10 or len(searchString) > 20:
            raise Exception("searchString is too short. Must be at least 2 characters")

        # check for possible sql attacks etc...
        if '}' in searchString or '{' in searchString or ';' in searchString:
            raise Exception("illegal characters in searchString")

        space_qs = BuildingFloorSpace.objects.filter(room_external_id=big_pk)

        if space_qs:
            att = space_qs.values()[0]

            if att['multi_poly']:
                att['multi_poly'] = None

            centroid_res = BuildingFloorSpace.objects.annotate(json=AsGeoJSON(Centroid('multi_poly'))).get(
                room_external_id=big_pk).json

            res = Feature(geometry=json.loads(centroid_res), properties=att)

            return Response(res)
        else:
            return Response(
                {'error': 'Sorry we did not find any record in our database matching your id = ' + str(big_pk)})
    else:
        # raise Exception("wrong IP! your ip is : " + ip_addr)
        # return HttpResponseForbidden()
        raise PermissionDenied
