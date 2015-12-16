#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import traceback
from django.http import HttpResponseNotFound, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from geojson import loads, Feature, FeatureCollection
from buildings.models import Building, BuildingFloorSpace
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import logging

from buildings.serializers import BuildingSerializer, BuildingFloorSpaceSerializer

logger = logging.getLogger(__name__)
from django.db import connection


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

@csrf_exempt
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
        serializer = BuildingFloorSpaceSerializer(floor_space_info, many=True)
        return Response(serializer.data)


def find_closest_network_node(x_coord, y_coord, floor):
    """
    Enter a given coordinate x,y and floor number and
    find the nearest network node id
    to start or end the route on
    :param x_coord: float  in epsg 3857
    :param y_coord: float  in epsg 3857
    :param floor: integer value equivalent to floor such as 2  = 2nd floor
    :return: node id as an integer
    """
    # connect to our Database
    logger.debug("now running function find_closest_network_node")
    cur = connection.cursor()

    # find nearest node on network within 200 m
    # and snap to nearest node
    query = """ SELECT
        verts.id as id
        FROM geodata.networklines_3857_vertices_pgr AS verts
        INNER JOIN
          (select ST_PointFromText('POINT({0} {1} {2})', 3857)as geom) AS pt
        ON ST_DWithin(verts.the_geom, pt.geom, 200.0)
        ORDER BY ST_3DDistance(verts.the_geom, pt.geom)
        LIMIT 1;""".format(x_coord, y_coord, floor)

    # pass 3 variables to our %s %s %s place holder in query
    cur.execute(query)

    # get the result
    query_result = cur.fetchone()

    # check if result is not empty
    if query_result is not None:
        # get first result in tuple response there is only one
        point_on_networkline = int(query_result[0])
        return point_on_networkline
    else:
        logger.debug("query is none check tolerance value of 200")
        return False


# use the rest_framework decorator to create our api
#  view for get, post requests
@api_view(['GET', 'POST'])
def create_route_from_coords(request, start_coord, start_floor, end_coord, end_floor, route_type):
    """
    Generate a GeoJSON indoor route passing in a start x,y,floor
    followed by &  then the end x,y,floor
    Sample request: http:/localhost:8000/api/v1/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2&0
    :param request:
    :param start_coord: start location x,y
    :param start_floor: floor number  ex)  2
    :param end_coord: end location x,y
    :param end_floor: end floor ex)  2
    :param route_type: type of route 1 = barrier-free ex) 1
    :return: GeoJSON route
    """

    if request.method == 'GET' or request.method == 'POST':

        cur = connection.cursor()

        # parse the incoming coordinates and floor using
        # split by comma
        x_start_coord = float(start_coord.split(',')[0])
        y_start_coord = float(start_coord.split(',')[1])
        start_floor_num = int(start_floor)

        x_end_coord = float(end_coord.split(',')[0])
        y_end_coord = float(end_coord.split(',')[1])
        end_floor_num = int(end_floor)

        # use our helper function to get vertices
        # node id for start and end nodes
        start_node_id = find_closest_network_node(x_start_coord,
                                                  y_start_coord,
                                                  start_floor_num)

        end_node_id = find_closest_network_node(x_end_coord,
                                                y_end_coord,
                                                end_floor_num)

        geojs_fc = run_route(start_node_id, end_node_id, route_type)

        try:
            return Response(geojs_fc)
        except:
            logger.error("error exporting to json model: " + str(geojs_fc))
            logger.error(traceback.format_exc())
            return Response({'error': 'either no JSON or no key params in your JSON'})
    else:
        return HttpResponseNotFound('<h1>Sorry not a GET or POST request</h1>')


def get_room_centroid_node(building_id, room_id):
    '''
    Find the room center point coordinates
    and find the closest route node point
    :param room_number: integer value of room number
    :return: Closest route node to submitted room number
    '''

    room_center_q = """SELECT  layer,
            ST_asGeoJSON(st_centroid(geom))
            AS geom FROM geodata.search_index_v
            WHERE building_id={0} and id ={1};""".format(building_id, room_id)

    cur = connection.cursor()
    cur.execute(room_center_q)

    res = cur.fetchall()

    res2 = res[0]

    room_floor = res2[0]
    room_geom_x = json.loads(res2[1])
    room_geom_y = json.loads(res2[1])

    x_coord = float(room_geom_x['coordinates'][0])
    y_coord = float(room_geom_y['coordinates'][1])

    room_node = find_closest_network_node(x_coord, y_coord, room_floor)
    try:
        return room_node
    except:
        logger.error("error get room center " + str(room_node))
        logger.error(traceback.format_exc())
        return {'error': 'error get room center'}


def run_route(start_node_id, end_node_id, route_type):
    '''

    :param start_node_id:
    :param end_node_id:
    :param route_type:
    :return:
    '''

    cur = connection.cursor()
    base_route_q = """SELECT id, source, target,
                     total_cost:: DOUBLE PRECISION AS cost,
                     floor, network_type
                     FROM geodata.networklines_3857"""

    # set default query
    barrierfree_q = "WHERE 1=1"
    if route_type == "1":
        # exclude all networklines of type stairs
        barrierfree_q = "WHERE network_type not in (1,3)"

    routing_query = '''
        SELECT seq,
        id1 AS node,
        id2 AS edge,
          ST_Length(geom) AS cost,
           floor,
          network_type,
          ST_AsGeoJSON(geom) AS geoj
          FROM pgr_dijkstra('
            {normal} {type}', %s, %s, FALSE, FALSE
          ) AS dij_route
          JOIN  geodata.networklines_3857 AS input_network
          ON dij_route.id2 = input_network.id ;
      '''.format(normal=base_route_q, type=barrierfree_q)

    # run our shortest path query
    if start_node_id or end_node_id:
        cur.execute(routing_query, (start_node_id, end_node_id))
    else:
        logger.error("start or end node is None "
                     + str(start_node_id))
        return HttpResponseNotFound('<h1>Sorry NO start or end node'
                                    ' found within 200m</h1>')

    # get entire query results to work with
    route_segments = cur.fetchall()

    # empty list to hold each segment for our GeoJSON output
    route_result = []

    # loop over each segment in the result route segments
    # create the list of our new GeoJSON
    for segment in route_segments:
        seg_cost = segment[3]  # cost value
        layer_level = segment[4]  # floor number
        seg_type = segment[5]
        geojs = segment[6]  # geojson coordinates
        geojs_geom = loads(geojs)  # load string to geom
        geojs_feat = Feature(geometry=geojs_geom,
                             properties={'floor': layer_level,
                                         'length': seg_cost,
                                         'network_type': seg_type})
        route_result.append(geojs_feat)

    # using the geojson module to create our GeoJSON Feature Collection
    geojs_fc = FeatureCollection(route_result)

    return geojs_fc


# use the rest_framework decorator to create our api
#  view for get, post requests
@api_view(['GET', 'POST'])
def create_route_from_id(request, building_id, start_room_id, end_room_id, route_type):
    '''
    Generate a GeoJSON route from external room id
    to external room id
    :param request: GET or POST request
    :param start_room_num: an integer room number
    :param end_room_num: an integer room number
    :param route_type: an integer room type
    :return: a GeoJSON linestring of the route
    '''

    if request.method == 'GET' or request.method == 'POST':


        start_room = int(start_room_id.split("=")[1])
        end_room = int(end_room_id.split("=")[1])
        building_id = int(building_id.split("=")[1])

        start_node_id = get_room_centroid_node(building_id, start_room)
        end_node_id = get_room_centroid_node(building_id, end_room)

        res = run_route(start_node_id, end_node_id, route_type)

        try:
            return Response(res)
        except:
            logger.error("error exporting to json model: " + str(res))
            logger.error(traceback.format_exc())
            return Response({'error': 'either no JSON or no key params in your JSON'})
    else:
        return HttpResponseNotFound('<h1>Sorry not a GET or POST request</h1>')


# use the rest_framework decorator to create our api
#  view for get, post requests
@api_view(['GET', 'POST'])
def create_route_from_search(request, building_id, start_term, end_term, route_type=0):
    '''
    Generate a GeoJSON route from room number
    to room number
    :param request: GET or POST request
    :param start_room_num: an integer room number
    :param end_room_num: an integer room number
    :param route_type: an integer room type
    :return: a GeoJSON linestring of the route
    '''

    if request.method == 'GET' or request.method == 'POST':


        start_room = start_term.split("=")[1]
        end_room = end_term.split("=")[1]
        building_id = building_id.split("=")[1]

        cur = connection.cursor()
        logger.debug('*************************start term' + str(start_room))
        logger.debug('*************************end term' + str(end_room))

        start_query = """SELECT id, external_id, search_string FROM geodata.search_index_v
                          WHERE replace(replace (upper(search_string), '.', ''),'.', '') LIKE upper('%{0}%')
                          ORDER BY length(search_string) LIMIT 1""".format(start_room)


        logger.debug('**************print query' + str(start_query))
        cur.execute(start_query)


        get_start_id_list = cur.fetchone()
        start_id_value = get_start_id_list[0]



        logger.debug('**************get start id' + str(start_id_value))


        end_query = """SELECT id, external_id, search_string FROM geodata.search_index_v
                          WHERE replace(replace (upper(search_string), '.', ''),'.', '') LIKE upper('%{0}%')
                          ORDER BY length(search_string) LIMIT 1""".format(end_room)

        logger.debug('**************print END  query' + str(end_query))
        cur.execute(end_query)

        get_end_id_list = cur.fetchone()
        end_id_value = get_end_id_list[0]

        logger.debug('*************************current start id' + str(start_id_value))
        logger.debug('*************************current end id' + str(end_id_value))

        start_node_id = get_room_centroid_node(building_id, start_id_value)
        end_node_id = get_room_centroid_node(building_id, end_id_value)

        res = run_route(start_node_id, end_node_id, route_type)

        try:
            return Response(res)
        except:
            logger.error("error exporting to json model: " + str(res))
            logger.error(traceback.format_exc())
            return Response({'error': 'either no JSON or no key params in your JSON'})
    else:
        return HttpResponseNotFound('<h1>Sorry not a GET or POST request</h1>')


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
