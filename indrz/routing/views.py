#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import traceback
import logging
import json
from django.http import HttpResponseNotFound
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geojson import loads, Feature, FeatureCollection



logger = logging.getLogger(__name__)


def get_room_centroid_node(building_id, space_id):
    '''
    Find the room center point coordinates
    and find the closest route node point
    :param room_number: integer value of room number
    :return: Closest route node to submitted room number
    '''

    room_center_q = """SELECT  layer,
            ST_asGeoJSON(st_centroid(geom))
            AS geom FROM geodata.search_index_v
            WHERE building_id={0} and id ={1};""".format(building_id, space_id)

    cur = connection.cursor()
    cur.execute(room_center_q)

    res = cur.fetchall()

    res2 = res[0]

    space_floor = res2[0]
    space_geom_x = json.loads(res2[1])
    space_geom_y = json.loads(res2[1])

    x_coord = float(space_geom_x['coordinates'][0])
    y_coord = float(space_geom_y['coordinates'][1])

    space_node_id = find_closest_network_node(x_coord, y_coord, space_floor)
    try:
        return space_node_id
    except:
        logger.error("error get room center " + str(space_node_id))
        logger.error(traceback.format_exc())
        return {'error': 'error get room center'}

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
    # logger.debug("now running function find_closest_network_node")
    cur = connection.cursor()

    # find nearest node on network within 200 m
    # and snap to nearest node

    query = """ SELECT
        verts.id as id
        FROM geodata.networklines_3857_vertices_pgr AS verts
        INNER JOIN
          (select ST_PointFromText('POINT({0} {1} {2})', 3857)as geom) AS pt
        ON ST_DWithin(verts.the_geom, pt.geom, 10) and st_Z(verts.the_geom)={2}
        ORDER BY ST_3DDistance(verts.the_geom, pt.geom)
        LIMIT 1;""".format(x_coord, y_coord, floor)

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


def format_walk_time(walk_time):
    """
    takes argument: float walkTime in seconds
    returns argument: string time  "xx minutes xx seconds"
    """
    if walk_time > 0.0:
        return str(int(walk_time / 60.0)) + " minutes " + str(int(round(walk_time % 60))) + " seconds"
    else:
        return "Walk time is less than zero! something is wrong"


def calc_distance_walktime(rows):
    """
    calculates distance and walk_time.
    rows must be an array of linestrings --> a route, retrieved from the DB.
    rows[5]: type of line (stairs, elevator, etc)
    rows[3]: cost as length of segment
    returns a dict with key/value pairs route_length, walk_time
    """

    route_length = 0
    walk_time = 0

    for row in rows:

        route_length += row[3]
        # calculate walk time
        if row[5] == 3 or row[5] == 4:  # stairs
            walk_speed = 1.2  # meters per second m/s
        elif row[5] == 5 or row[5] == 6:  # elevator
            walk_speed = 1.1  # m/s
        else:
            walk_speed = 1.39  # m/s

        walk_time += (row[3] / walk_speed)

    length_format = "%.2f" % route_length
    real_time = format_walk_time(walk_time)
    return {"route_length": length_format, "walk_time": real_time}


def merge_geojson(geojs1, geojs2):
    feat = geojs1['features'] # list of geom
    feat2 = geojs2['features'] # list of geom

    route_merge = []

    route_merge.extend(feat)
    route_merge.extend(feat2)


    return route_merge

@api_view(['GET', 'POST'])
def force_route_mid_point(request, search_result=None):
    """
    Force a route over a middle point such as a front office
    :return: a GeoJSON route with a middle point
    """

    demo_options = {'route_types':
        {'standard_route' : 1,
         'barrierfree route' : 2,
         'indoor_only_prefered': 3,
         'fastest': 4
         }

    ,
    'route_logic':{
        'force_route_through_location': True,
        'set_route_mid_point': True
    },
                    'extra_location':{
                        'node_id': 1234,
                        'floor_num': 1,
                        'space_id' : 123

                    }}
    building_id = 1
    search_result = {'building-id': 1, 'start-node-id': 1385, 'mid-node-id': 1167, 'end-node-id': 1252}

    # remove last coordinate of first route
    start_node_id = get_room_centroid_node(building_id, search_result['start-node-id'])
    mid_node_id = get_room_centroid_node(building_id, search_result['mid-node-id'])
    end_node_id = get_room_centroid_node(building_id, search_result['end-node-id'])

    route_start_to_mid_point = run_route(start_node_id, mid_node_id, 1)
    route_mid_to_end_point = run_route(mid_node_id, end_node_id, 1)

    route_out_merge = merge_geojson(route_start_to_mid_point, route_mid_to_end_point )
    # return all but the first and last item in python list
    #my_list = my_list[1:-1]
    f = []
    route_to_mid_features = route_start_to_mid_point['features'][1:-1]
    route_to_end_features = route_mid_to_end_point['features']

    f.append(route_start_to_mid_point)
    f.append(route_mid_to_end_point)


    #route_to_mid_point['features'][-1:] # returns the last line segment in route
    #route_to_mid_point['features'][-1:][0]['geometry']['coordinates'][-1] # returns last coordinate on route

    return Response({'type' : 'FeatureCollection', 'features': route_out_merge})


def run_route(start_node_id, end_node_id, route_type, route_options=None):
    '''

    :param start_node_id:
    :param end_node_id:
    :param route_type:
    :param route_options: a dictionary
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
        if start_node_id != end_node_id:
            cur.execute(routing_query, (start_node_id, end_node_id))
    else:
        logger.error("start or end node is None or is the same node "
                     + str(start_node_id))
        return HttpResponseNotFound('<h1>Sorry NO start or end node'
                                    ' found within 200m</h1>')

    # get entire query results to work with
    route_segments = cur.fetchall()


    route_info = calc_distance_walktime(route_segments)

    # empty list to hold each segment for our GeoJSON output
    route_result = []

    # loop over each segment in the result route segments
    # create the list of our new GeoJSON
    for segment in route_segments:
        seg_length = segment[3]  # length of segment
        layer_level = segment[4]  # floor number
        seg_type = segment[5]
        seg_node_id = segment[1]
        seq_sequence = segment[0]
        geojs = segment[6]  # geojson coordinates
        geojs_geom = loads(geojs)  # load string to geom
        geojs_feat = Feature(geometry=geojs_geom,
                             properties={'floor': layer_level,
                                         'length': seg_length,
                                         'network_type': seg_type,
                                         'seg_node_id': seg_node_id,
                                         'sequence': seq_sequence}
                                         )
        route_result.append(geojs_feat)

    # using the geojson module to create our GeoJSON Feature Collection
    geojs_fc = FeatureCollection(route_result)
    geojs_fc.update(route_info)
    return geojs_fc


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
        # logger.debug('*************************start term' + str(start_room))
        # logger.debug('*************************end term' + str(end_room))

        start_query = """SELECT id, external_id, search_string FROM geodata.search_index_v
                          WHERE replace(replace (upper(search_string), '.', ''),'.', '') LIKE upper('%{0}%')
                          ORDER BY length(search_string) LIMIT 1""".format(start_room)


        # logger.debug('**************print query' + str(start_query))
        cur.execute(start_query)


        get_start_id_list = cur.fetchone()
        start_id_value = get_start_id_list[0]



        # logger.debug('**************get start id' + str(start_id_value))


        end_query = """SELECT id, external_id, search_string FROM geodata.search_index_v
                          WHERE replace(replace (upper(search_string), '.', ''),'.', '') LIKE upper('%{0}%')
                          ORDER BY length(search_string) LIMIT 1""".format(end_room)

        # logger.debug('**************print END  query' + str(end_query))
        cur.execute(end_query)

        get_end_id_list = cur.fetchone()
        end_id_value = get_end_id_list[0]

        # logger.debug('*************************current start id' + str(start_id_value))
        # logger.debug('*************************current end id' + str(end_id_value))

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