#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import traceback
import logging
from django.http import HttpResponseNotFound, HttpResponse

from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response

from buildings.models import Building, BuildingFloorSpace, BuildingFloor
from buildings.serializers import (BuildingSerializer,
                                   BuildingShortSerializer,
                                   BuildingFloorSpaceSerializer,
                                   BuildingFloorSerializer,
                                   SpaceSerializer)

logger = logging.getLogger(__name__)

@api_view(['GET', ])
def building_short_list(request, format=None):
    """
    List all buildings without details
    """
    if request.method == 'GET':
        buildings = Building.objects.all()
        serializer = BuildingShortSerializer(buildings, many=True)
        return Response(serializer.data)

    # elif request.method == 'POST':
    #     serializer = BuildingSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def building_list(request, format=None):
    """
    List all buildings, or create a new building.
    """
    if request.method == 'GET':
        buildings = Building.objects.all()
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)

    # elif request.method == 'POST':
    #     serializer = BuildingSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def building_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        building = Building.objects.get(pk=pk)
    except Building.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BuildingSerializer(building)
        return Response(serializer.data)

    # elif request.method == 'PUT':
    #     serializer = BuildingSerializer(building, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # elif request.method == 'DELETE':
    #     building.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def building_floors_list(request, building_id, format=None):
    """
    List all floor ids for a specific building
    """
    if request.method == 'GET':
        floor_ids = BuildingFloor.objects.filter(fk_building=building_id)
        serializer = BuildingFloorSerializer(floor_ids, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def building_spaces_list(request, building_id, floor_id, format=None):
    """
    List all spaces on a specified floor in given building.
    """
    if request.method == 'GET':
        floor_spaces = BuildingFloorSpace.objects.filter(fk_building=building_id, fk_building_floor=floor_id)
        serializer = BuildingFloorSpaceSerializer(floor_spaces, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_floor_space_id(request, space_id, format=None):
    """
    Return the GeoJSON of a single space ex. a single room
    """
    if request.method == 'GET':
        floor_space_info = BuildingFloorSpace.objects.filter(id=space_id)
        serializer = SpaceSerializer(floor_space_info, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_external_id(request, building_id, external_room_id, format=None):
    """
    Return the GeoJSON of a single space passing your local room id we call it external id
    """
    if request.method == 'GET':
        floor_space_info = BuildingFloorSpace.objects.filter(room_external_id=external_room_id, fk_building_id=building_id)
        serializer = SpaceSerializer(floor_space_info, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_space_by_name(request, building_id, space_name, format=None):
    """
    Return the GeoJSON of a single space passing your local space name
    """
    if request.method == 'GET':
        floor_space_info = BuildingFloorSpace.objects.filter(short_name=space_name, fk_building_id=building_id)
        serializer = SpaceSerializer(floor_space_info, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def autocomplete_list(request):
    '''-
    http://localhost:8000/api/v1/spaces/
    :param request: no parameters GET or POST
    :return: JSON Array of available search terms
    '''
    cur = connection.cursor()
    if request.method == 'GET' or request.method == 'POST':

        # searchString = request.GET.get('q','')

        # cur.execute("""SELECT search_string FROM geodata.search_index_v
        #                   WHERE replace(replace (upper(search_string), '.', ''),'.', '') LIKE upper(%(search_string)s)
        #                   GROUP BY search_string
        #                   ORDER BY length(search_string) LIMIT 100""",
        #                {"search_string": "%" + searchString + "%"})

        cur.execute("""SELECT search_string FROM geodata.search_index_v
                          """
                      )
        # cur.execute(room_query)
        room_nums = cur.fetchall()

        room_num_list = []
        for x in room_nums:
            v = x[0]
            room_num_list.append(v)

        try:
            #return Response(room_num_list)
            return HttpResponse(json.dumps(room_num_list), content_type='application/json')
        except:
            logger.error("error exporting to json model: " + str(room_num_list))
            logger.error(traceback.format_exc())
            return Response({'error': 'either no JSON or no key params in your JSON'})


@api_view(['GET', 'POST'])
def list_buildings(request):
    '''-
    http://localhost:8000/api/v1/spaces/
    :param request: no parameters GET or POST
    :return: JSON Array of available search terms
    '''
    cur = connection.cursor()
    if request.method == 'GET' or request.method == 'POST':

        searchString = request.GET.get('q','')

        cur.execute("""SELECT id, building_name, num_floors FROM geodata.search_index_v
                          WHERE replace(replace (upper(search_string), '.', ''),'.', '') LIKE upper(%(search_string)s)
                          GROUP BY search_string
                          ORDER BY length(search_string) LIMIT 100""",
                       {"search_string": "%" + searchString + "%"})

        # cur.execute(room_query)
        room_nums = cur.fetchall()

        room_num_list = []
        for x in room_nums:
            v = x[0]
            room_num_list.append(v)

        try:
            #return Response(room_num_list)
            return HttpResponse(json.dumps(room_num_list), content_type='application/json')
        except:
            logger.error("error exporting to json model: " + str(room_num_list))
            logger.error(traceback.format_exc())
            return Response({'error': 'either no JSON or no key params in your JSON'})
