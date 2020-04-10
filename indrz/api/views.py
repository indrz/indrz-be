#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re

from buildings.models import BuildingFloor
from buildings.models import BuildingFloorSpace
from buildings.serializers import FloorListSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
