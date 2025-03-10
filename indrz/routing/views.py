#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import traceback
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language_from_request
from geojson import loads, Feature, FeatureCollection, Point
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from buildings.models import BuildingFloorSpace
from poi_manager.models import Poi
from poi_manager.serializers import PoiSerializer

from .route_utils import (nearest_edge, find_closest_network_node, get_room_centroid_node, calc_distance_walktime,
                         find_closest_poi, create_route_markers)

logger = logging.getLogger(__name__)



@api_view(['GET', 'POST'])
def create_route_library(request, start_coords, end_coords, route_type=0):
    # create a cursor
    cur = connection.cursor()



    start_coords_str = start_coords.split(",")
    end_coords_str = end_coords.split(",")

    # start_x = float(start_coords_str[0])
    # start_y = float(start_coords_str[1])
    # start_z = int(start_coords_str[2])

    end_x = float(end_coords_str[0])
    end_y = float(end_coords_str[1])
    end_z = int(end_coords_str[2])

    start_x = 1587954.174
    start_y = 5879616.333
    start_z = 1
    #
    # end_x = 1587974.747
    # end_y = 5879662.800
    # end_z = 2

    #
    # start_coords = (1587929.168,5879642.328,1)
    # end_coords = (1587963.046,5879655.956,3)
    #
    # start_coords = (1587936.357, 5879665.841,3)  # x, y
    # end_coords = (1587954.286, 5879661.907,3 )  # x,y
    start_coord = ""
    end_coord = ""

    route_query = "SELECT id, source, target, cost, reverse_cost FROM geodata.networklines_3857"

    nearest_node_sql = f"""SELECT
        verts.id as id
        FROM geodata.networklines_3857_vertices_pgr AS verts
        INNER JOIN
          (select ST_PointFromText('POINT({0} {1} {2})', 3857)as geom) AS pt
        ON ST_DWithin(verts.the_geom, pt.geom, 50) and st_Z(verts.the_geom)={2}
        ORDER BY ST_3DDistance(verts.the_geom, pt.geom)
        LIMIT 1"""

    routing_query = """ WITH
                dijkstra AS (
                    SELECT * FROM pgr_dijkstra(
                        '{sql_query} {where}', (SELECT
                      verts1.id
                      FROM geodata.networklines_3857_vertices_pgr AS verts1
                      INNER JOIN
                        (select ST_PointFromText('POINT({startX} {startY} {startZ})', 3857)as geom) AS pt
                      ON ST_DWithin(verts1.the_geom, pt.geom, 50) and st_Z(verts1.the_geom)={startZ}
                      ORDER BY ST_3DDistance(verts1.the_geom, pt.geom)
                      LIMIT 1), (
                    SELECT
                          verts.id
                          FROM geodata.networklines_3857_vertices_pgr AS verts
                          INNER JOIN
                            (select ST_PointFromText('POINT({endX} {endY} {endZ})', 3857)as geom) AS pt
                          ON ST_DWithin(verts.the_geom, pt.geom, 50) and st_Z(verts.the_geom)={endZ}
                          ORDER BY ST_3DDistance(verts.the_geom, pt.geom)
                          LIMIT 1
                ))),
                get_geom AS (
                    SELECT dijkstra.*, input_network.network_type as network_type, input_network.id as id, input_network.floor as floor,
                        -- adjusting directionality
                        CASE
                            WHEN dijkstra.node = input_network.source THEN geom
                            ELSE ST_Reverse(geom)
                        END AS route_geom
                    FROM dijkstra JOIN geodata.networklines_3857 AS input_network ON (dijkstra.edge = input_network.id)
                    ORDER BY seq)
                SELECT seq, id, node, edge, 
                    ST_Length(st_transform(route_geom,4326), TRUE ) AS cost,  
                    agg_cost, 
                    floor, 
                    network_type,
                    ST_AsGeoJSON(route_geom) AS geoj, 
                    degrees(ST_azimuth(ST_StartPoint(route_geom), ST_EndPoint(route_geom))) AS azimuth,
                    route_geom
                    FROM get_geom
                    ORDER BY seq;""".format(sql_query=route_query, where="WHERE 1=1",
                                        startX=start_x, startY = start_y, startZ = start_z,
                                        endX = end_x, endY = end_y, endZ = end_z)

    cur.execute(routing_query)

    route_segments = cur.fetchall()


    nearest_end_edge = nearest_edge((end_x, end_y, end_z), 'end')

    first_edge_geom = route_segments[0][10]
    last_edge_geom = route_segments[-1][10]

    # snap end coord to nearest network edge  get coordinate location of xyz on network edge
    sql_xyz_end_on_edge = """ST_LineLocatePoint('{edge}', ST_SetSRID(ST_MakePoint({x}, {y}, {z}),3857))""".format(edge=nearest_end_edge[1], x=end_x, y=end_y, z=end_z) # returns point

    # get coordinate of last node on network nodes xyz
    # create line from last node xyz to xyz end coord on network edge
    # insert line segment to route as last segment



    # returns geometry ST_LineSubstring(geometry a_linestring, float8 startfraction, float8 endfraction);

    sql_get_new_start_segment = """ SELECT ST_AsGeoJSON(ST_LineSubstring('{edge}', ST_LineLocatePoint('{edge}', ST_SetSRID(ST_MakePoint({x}, {y}, {z}),3857)), 1)) """.format(edge=first_edge_geom, x=start_x, y=start_y, z=start_z)
    sql_get_new_end_segment = """ SELECT ST_AsGeoJSON(ST_LineSubstring('{edge}', 0, ST_LineLocatePoint('{edge}', ST_SetSRID(ST_MakePoint({x}, {y}, {z}),3857))))""".format(edge=nearest_end_edge[1], x=end_x, y=end_y, z=end_z)

    cur.execute(sql_get_new_start_segment)
    start_seg = cur.fetchone()

    cur.execute(sql_get_new_end_segment)
    end_seg = cur.fetchone()



    n_rsegs = list(route_segments)



    route_segments2 = list(n_rsegs[0])
    route_segments3 = list(n_rsegs[-1])

    route_segments2.pop(8)  # remove first one
    route_segments3.pop(8)  # remove last one

    route_segments2.insert(8, start_seg[0])
    route_segments3.insert(8, end_seg[0])

    # n_rsegs.pop(0)
    # n_rsegs.insert(0, route_segments2)
    #
    # n_rsegs.pop(-1)
    # n_rsegs.insert(-1, route_segments3)


    # TODO if start and end coords are on one single segement
    # take the segment ST_LineSubstring(single_edge, start float, end float)

    # TODO if start coord is same as start node coord

    # TODO if end coord is same as end node coord

    route_result = []

    for segment in n_rsegs:
        seg_length = segment[4]  # length of segment
        layer_level = segment[6]  # floor number
        seg_type = segment[7]
        seg_node_id = segment[2]
        seq_sequence = segment[0]
        geojs = segment[8]  # geojson coordinates
        azimuth = segment[9]
        # geojs = big_test[0]
        geojs_geom = loads(geojs, object_pairs_hook=OrderedDict)  # load string to geom
        geojs_feat = Feature(geometry=geojs_geom,
                             properties={'floor': layer_level,
                                         'segment_length': seg_length,
                                         'network_type': seg_type,
                                         'seg_node_id': seg_node_id,
                                         'sequence': seq_sequence,
                                         'azimuth': azimuth}
                             )
        route_result.append(geojs_feat)

    # using the geojson module to create our GeoJSON Feature Collection
    geojs_fc = FeatureCollection(route_result)

    route_info = calc_distance_walktime(n_rsegs)

    geojs_fc.update(route_info)

    geojs_fc['route_info']['start_name'] = "Entrance Library"
    geojs_fc['route_info']['mid_name'] = ""
    geojs_fc['route_info']['end_name'] = "some book"

    start_marker_xy = (start_x, start_y)
    end_marker_xy = (end_x, end_y)

    marks = create_route_markers(start_marker_xy, end_marker_xy, start_z, end_z, "Entrance Library", "some book")

    geojs_fc['route_info']['route_markers'] = marks

    try:
        return Response(geojs_fc)
    except:
        logger.error("error exporting to json model: " + str(geojs_fc))
        logger.error(traceback.format_exc())
        return Response({'error': 'either no JSON or no key params in your JSON'})



# use the rest_framework decorator to create our api
#  view for get, post requests
@api_view(['GET', 'POST'])
def create_route_from_coords(request, start_coord, start_floor, end_coord, end_floor, route_type, reverse_route="false"):
    """
    Generate a GeoJSON indoor route passing in a start x,y,floor
    followed by &  then the end x,y,floor
    Sample request: http:/localhost:8000/api/v1/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2&0
    :param request:
    :param reverse_route: string  "true" or "false"
    :param start_coord: start location x,y
    :param start_floor: floor number  ex)  2
    :param end_coord: end location x,y
    :param end_floor: end floor ex)  2
    :param route_type: type of route 1 = barrier-free ex) 1
    :return: GeoJSON route
    """

    if request.method == 'GET' or request.method == 'POST':

        route_type_val = 0
        if isinstance(route_type, str):
            if route_type.endswith('1'):
                route_type_val = 1
            if route_type.endswith('0'):
                route_type_val = 0
        else:
            route_type_val = route_type

        rev_val = str(reverse_route)

        # parse the incoming coordinates and floor using
        # split by comma
        x_start_coord = float(start_coord.split(',')[0])
        y_start_coord = float(start_coord.split(',')[1])
        start_floor_num = int(start_floor)

        x_end_coord = float(end_coord.split(',')[0])
        y_end_coord = float(end_coord.split(',')[1])
        end_floor_num = int(end_floor)

        start_data = [x_start_coord, y_start_coord, start_floor_num]
        end_data = [x_end_coord, y_end_coord, end_floor_num]

        if start_data == end_data:
            return Response({"error": "route from coords", "reason": "Error: The coordinates start and end locations are the same" }, status=status.HTTP_200_OK)

        coord_data = [start_data, end_data]

        # use our helper function to get vertices
        # node id for start and end nodes
        start_node_id = find_closest_network_node(x_start_coord,
                                                  y_start_coord,
                                                  start_floor_num)

        end_node_id = find_closest_network_node(x_end_coord,
                                                y_end_coord,
                                                end_floor_num)

        if rev_val == "true":
            # reverse the route
            geojs_fc = run_route(end_node_id, start_node_id, route_type_val, None, coord_data)
        else:
            geojs_fc = run_route(start_node_id, end_node_id, route_type_val, None, coord_data)

        if "error" in geojs_fc.keys():
            return Response({"error": geojs_fc}, status=status.HTTP_200_OK)
        else:
            start_coords = {'coordinates': [[x_start_coord, y_start_coord]], 'type': 'MultiPoint'}
            end_coords = {'coordinates': [[x_end_coord, y_end_coord]], 'type': 'MultiPoint'}

            start_name = str(x_start_coord) + "," + str(y_start_coord) + "," + str(start_floor_num)
            end_name = str(x_end_coord) + "," + str(y_end_coord) + "," + str(end_floor_num)

            geojs_fc['route_info']['start_name'] = start_name
            geojs_fc['route_info']['mid_name'] = ""
            geojs_fc['route_info']['end_name'] = end_name

            if rev_val == "false":

                marks = create_route_markers(start_coords, end_coords, start_floor_num, end_floor_num, start_name,
                                             end_name)
            else:
                marks = create_route_markers(end_coords, start_coords, start_floor_num, end_floor_num, start_name,
                                             end_name)

            geojs_fc['route_info']['route_markers'] = marks

            try:
                return Response(geojs_fc)
            except:
                logger.error("error exporting to json model: " + str(geojs_fc))
                logger.error(traceback.format_exc())
                return Response({'error': 'either no JSON or no key params in your JSON'})
    else:
        return HttpResponseNotFound('<h1>Sorry not a GET or POST request</h1>')



def merge_2_routes(route_part1, route_part2):
    """
    Merges two route feature geometries into a single GeoJSON
    features list.
    :param route_part1 a valid route GeoJSON route result from A to B
    :param route_part2 a valid GeoJSON route result from B to C
    :return: the GeoJSON features key with all route segements
        of both routes from A to B and B to C where A is start
        B is middle destination and C is final destination
    """

    if route_part1:
        geo_features_route_part_1 = route_part1['features']  # list of geom
        geo_features_route_part_2 = route_part2['features']  # list of geom

        routes_merged = []

        routes_merged.extend(geo_features_route_part_1)
        routes_merged.extend(geo_features_route_part_2)

        return routes_merged
    else:
        return None


@api_view(['GET', 'POST'])
def force_route_mid_point(request, **kwargs):
    """
    Force a route over a middle point such as a front office
    :return: a single GeoJSON featureCollection with a middle point
    :param
    """
    start_node = request.GET.get('startnode', 1)  # 1385
    mnode = request.GET.get('midnode', 1)  # 1167
    end_node = request.GET.get('endnode', 1)  # 1252

    # building_id = 1
    route_nodes = {'building-id': 1, 'start-node-id': start_node, 'mid-node-id': mnode, 'end-node-id': end_node}

    # remove last coordinate of first route
    start_node_id = get_room_centroid_node(route_nodes['start-node-id'])
    mid_node_id = get_room_centroid_node(route_nodes['mid-node-id'])
    end_node_id = get_room_centroid_node(route_nodes['end-node-id'])

    route_start_to_mid_point = run_route(start_node_id, mid_node_id, 1)
    route_mid_to_end_point = run_route(mid_node_id, end_node_id, 1)

    if "error" in route_start_to_mid_point or "error" in route_mid_to_end_point:
        return Response({"error": "no route"}, status=status.HTTP_200_OK)
    else:
        route_out_merge = merge_2_routes(route_start_to_mid_point, route_mid_to_end_point)
        return Response({'type': 'FeatureCollection', 'features': route_out_merge})


class RoutePoiToPoi(APIView):
    """
    Route from one POI to any other POI
    """

    def get(self, request, start_poi_id, end_poi_id, reversed=False, route_type=0):
        """
        Sample Request URL: /directions/start-poi-id=234&end-poi-id=1122&type=0?format=json
        Optionally restricts the returned purchases to a given poi,
        by filtering against a `name` query parameter in the URL.

        :param request:
        :param start-poi-id: integer start-poi-id
        :param end-poi-id: integer end-poi-id
        :param route_type: integer 0 normal route 1 barrierer free route
        :return:
        """

        start_poi = int(start_poi_id.split("=")[1])
        end_poi = int(end_poi_id.split("=")[1])

        if start_poi == end_poi:
            return Response({"error": "route poi to poi", "reason": "Error: The POI start and end locations are the same" }, status=status.HTTP_200_OK)

        r_type = 0
        if isinstance(route_type, str):
            if route_type.endswith('1'):
                r_type = 1
            if route_type.endswith('0'):
                r_type = 0
        if isinstance(route_type, int):
            r_type = route_type


        try:
            start_poi = Poi.objects.get(pk=start_poi)
        except ObjectDoesNotExist:
            return Response({"error": "no poi found with given id"}, status=status.HTTP_200_OK)

        try:
            end_poi = Poi.objects.get(pk=end_poi)
        except ObjectDoesNotExist:
            return Response({"error": "no poi found with given id"}, status=status.HTTP_200_OK)


        start_node_id = find_closest_network_node(start_poi.geom.coords[0][0], start_poi.geom.coords[0][1],
                                                  start_poi.floor_num)

        end_node_id = find_closest_network_node(end_poi.geom.coords[0][0], end_poi.geom.coords[0][1],
                                                  end_poi.floor_num)

        geojs_fc = run_route(start_node_id, end_node_id, route_type=r_type)

        if "error" in geojs_fc:
            return Response(geojs_fc, status=status.HTTP_200_OK)
        else:
            serializer_s = PoiSerializer(start_poi)
            serializer_e = PoiSerializer(end_poi)

            geojs_fc['route_info']['start_name'] = start_poi.name
            geojs_fc['route_info']['end_name'] = end_poi.name
            geojs_fc['route_info']['start'] = serializer_s.data
            geojs_fc['route_info']['end'] = serializer_e.data
            geojs_fc['route_info']['mid_name'] = ""

            start_name = start_poi.name
            end_name = end_poi.name
            poi_floor = end_poi.floor_num

            start_coords = {'coordinates': [[start_poi.geom.coords[0][0], start_poi.geom.coords[0][1]]],
                            'type': 'MultiPoint'}

            poi_geom = {'coordinates': [end_poi.geom.coords[0]], 'type': 'MultiPoint'}

            marks = create_route_markers(poi_geom, start_coords, poi_floor, start_poi.floor_num, end_name,
                                         start_name)

            if reversed:
                geojs_fc['route_info']['start_name'] = end_poi.name
                geojs_fc['route_info']['end_name'] = start_poi.name
                geojs_fc['route_info']['start'] = serializer_e.data
                geojs_fc['route_info']['end'] = serializer_s.data
                start_name = end_poi.name
                end_name = start_poi.name
                poi_floor = start_poi.floor_num

                marks = create_route_markers(start_coords, poi_geom, start_poi.floor_num, poi_floor, start_name,
                                             end_name)

            geojs_fc['route_info']['route_markers'] = marks

            return Response(geojs_fc, status=status.HTTP_200_OK)


# write a test for RoutePoiToPoi
def test_route_poi_to_poi():
    """
    Test RoutePoiToPoi
    :return:
    """
    pass

class RoutePoiToPoiV0(RoutePoiToPoi):
    pass


class NearestPoi(APIView):
    """
    Locate the closest poi to a specific location providing a poi category id number
        :param request: get request
        :param coordinates: coordinate pair x,y format  1234.56,987.54
        :param floor: integer number between -1 and 8
        :param poi_cat_id: integer
        :example /api/v1/directions/near/coords=1826699.1815499999,6142531.790750001&floor=5&poiCatId=13/?format=json

    """
    def get(self, request, coordinates, floor, poi_cat_id):
        """

        :param request: get request
        :param coordinates: coordinate pair x,y format  1234.56,987.54
        :param floor: integer number between -1 and 8
        :param poi_cat_id: integer
        :return: JSON poi data
        :example /api/v1/directions/near/coords=1826699.1815499999,6142531.790750001&floor=5&poiCatId=13/?format=json
        """

        coords = coordinates.split("=")[1]
        x_start_coord = float(coords.split(',')[0])
        y_start_coord = float(coords.split(',')[1])
        start_floor_num = int(floor.split('=')[1])
        poi_cat_id_v = int(poi_cat_id.split("=")[1])
        lang_code = get_language_from_request(request)

        poi_data = find_closest_poi(coords, start_floor_num, poi_cat_id_v, lang_code)

        if "error" not in poi_data:

            return Response(poi_data)
        else:
            return Response({"error": f"{poi_data['error']}"}, status=status.HTTP_400_BAD_REQUEST)


#TODO remove this old legacy api
class RoutePoiToXyzV0(APIView):
    """

    :param reversed_dir: boolean to set the direction of route query to allow routing
    from xyz to a poi
    :param request:
    :param start_poi_id: unique single poi id value, integer
    :param end_xyz: end coordinate pair  x,y  ex) 1826685.08369146,6142499.125477515
    :param z_floor: integer value used to create the z value of xyz coordinate
    :return: GeoJson route from poi id to xyz coordinate

    Usage:
    http://localhost:8000/en/indrz/api/v1/directions/poi-id=27&xyz=1826685.08369146,6142499.125477515&floor=3
    http://localhost:8000/en/indrz/api/v1/directions/poi-id=27&xyz=1826685.08369146,6142499.125477515&floor=3&reversed=true

    """

    def get(self, request, start_poi_id, end_xyz, z_floor, reversed_dir=False, route_type=0):
        """

        :param reversed_dir: boolean to set the direction of route query to allow routing
        from xyz to a poi
        :param request:
        :param start_poi_id: unique single poi id value, integer
        :param end_xyz: end coordinate pair  x,y  ex) 1826685.08369146,6142499.125477515
        :param z_floor: integer value used to create the z value of xyz coordinate
        :param route_type: 0 for shortest route, 1 for barrierfree route ie no stairs
        :return: GeoJson route from poi id to xyz coordinate

        Usage:   http://localhost:8000/api/v1/directions/poi-id=12764&xyz=1822036.251214,6140092.37464&floor=5&reversed=false&type=0
        """

        start_poi = int(start_poi_id.split("=")[1])
        xyz_str = end_xyz.split('=')[1]
        x_end_coord = float(xyz_str.split(",")[0])
        y_end_coord = float(xyz_str.split(",")[1])
        z_end_floor = z_floor.split("=")[1]

        r_type = 0
        if isinstance(route_type, str):
            if route_type.endswith('1'):
                r_type = 1
            if route_type.endswith('0'):
                r_type = 0
        if isinstance(route_type, int):
            r_type = route_type



        if start_poi is not None:

            try:
                qs_start = Poi.objects.get(pk=start_poi)
            except ObjectDoesNotExist:
                return Response({"error": "no poi found with given id", "reason":"Sorry no POI found"}, status=status.HTTP_200_OK)

            start_node_id = find_closest_network_node(qs_start.geom.coords[0][0], qs_start.geom.coords[0][1],
                                                      qs_start.floor_num)

            end_node_id = find_closest_network_node(x_end_coord, y_end_coord, z_end_floor)

            if reversed_dir:
                geojs_fc = run_route(end_node_id, start_node_id, r_type)
            else:
                geojs_fc = run_route(start_node_id, end_node_id, r_type)

            if "error" in geojs_fc:
                return Response(geojs_fc, status=status.HTTP_200_OK)
            else:
                serializer_s = PoiSerializer(qs_start)

                pt = Point((x_end_coord, y_end_coord))

                end_geojs_feat = Feature(geometry=pt,
                                     properties={'floor': z_end_floor, 'coordinates': xyz_str}
                                     )

                geojs_fc['route_info']['start_name'] = qs_start.name
                geojs_fc['route_info']['end_name'] = xyz_str

                geojs_fc['route_info']['start'] = serializer_s.data
                geojs_fc['route_info']['end'] = end_geojs_feat
                geojs_fc['route_info']['mid_name'] = ""

                return Response(geojs_fc, status=status.HTTP_200_OK)
        else:
            return Response({"error": "no poi its None"}, status=status.HTTP_400_BAD_REQUEST)


class RoutePoiToXyz(APIView):
    """

    :param reversed_dir: boolean to set the direction of route query to allow routing
    from xyz to a poi
    :param request:
    :param start_poi_id: unique single poi id value, integer
    :param end_xyz: end coordinate pair  x,y  ex) 1826685.08369146,6142499.125477515
    :param z_floor: integer value used to create the z value of xyz coordinate
    :return: GeoJson route from poi id to xyz coordinate

    Usage:
    http://localhost:8000/en/indrz/api/v1/directions/poi-id=27&xyz=1826685.08369146,6142499.125477515&floor=3
    http://localhost:8000/en/indrz/api/v1/directions/poi-id=27&xyz=1826685.08369146,6142499.125477515&floor=3&reversed=true

    """

    def get(self, request, start_poi_id, end_xyz, reversed=False, route_type=0):
        """

        :param reversed_dir: boolean to set the direction of route query to allow routing
        from xyz to a poi
        :param request:
        :param start_poi_id: unique single poi id value, integer
        :param end_xyz: end coordinate pair  x,y  ex) 1826685.08369146,6142499.125477515
        :param z_floor: integer value used to create the z value of xyz coordinate
        :param route_type: 0 for shortest route, 1 for barrierfree route ie no stairs
        :return: GeoJson route from poi id to xyz coordinate

        Usage:   http://localhost:8000/api/v1/directions/poi-id=12764&xyz=1822036.251214,6140092.37464&floor=5&reversed=false&type=0
        """

        start_poi = int(start_poi_id.split("=")[1])
        xyz_str = end_xyz.split('=')[1]
        x_end_coord = float(xyz_str.split(",")[0])
        y_end_coord = float(xyz_str.split(",")[1])
        z_end_floor = float(xyz_str.split(",")[2])
        # z_end_floor = z_floor.split("=")[1]

        r_type = 0
        if isinstance(route_type, str):
            if route_type.endswith('1'):
                r_type = 1
            if route_type.endswith('0'):
                r_type = 0
        if isinstance(route_type, int):
            r_type = route_type



        if start_poi is not None:

            try:
                qs_start = Poi.objects.get(pk=start_poi)
            except ObjectDoesNotExist:
                return Response({"error": "no poi found with given id", "reason":"Sorry no POI found"}, status=status.HTTP_200_OK)

            start_node_id = find_closest_network_node(qs_start.geom.coords[0][0], qs_start.geom.coords[0][1],
                                                      qs_start.floor_num)

            end_node_id = find_closest_network_node(x_end_coord, y_end_coord, z_end_floor)

            if reversed:
                geojs_fc = run_route(end_node_id, start_node_id, r_type)
            else:
                geojs_fc = run_route(start_node_id, end_node_id, r_type)

            if "error" in geojs_fc.keys():
                return Response(geojs_fc, status=status.HTTP_200_OK)
            else:
                serializer_s = PoiSerializer(qs_start)

                pt = Point((x_end_coord, y_end_coord))

                end_geojs_feat = Feature(geometry=pt,
                                     properties={'floor': z_end_floor, 'coordinates': xyz_str}
                                     )

                geojs_fc['route_info']['start_name'] = qs_start.name
                geojs_fc['route_info']['end_name'] = xyz_str

                geojs_fc['route_info']['start'] = serializer_s.data
                geojs_fc['route_info']['end'] = end_geojs_feat
                geojs_fc['route_info']['mid_name'] = ""

                return Response(geojs_fc, status=status.HTTP_200_OK)
        else:
            return Response({"error": "no poi its None", "reason":"Sorry no POI"}, status=status.HTTP_200_OK)



class RouteSpaceToXyz(APIView):
    """

    :param reversed_dir: boolean to set the direction of route query to allow routing
    from xyz to a poi
    :param request:
    :param start_poi_id: unique single poi id value, integer
    :param end_xyz: end coordinate pair  x,y  ex) 1826685.08369146,6142499.125477515
    :param z_floor: integer value used to create the z value of xyz coordinate
    :return: GeoJson route from poi id to xyz coordinate

    Usage:
    http://localhost:8000/en/indrz/api/v1/directions/poi-id=27&xyz=1826685.08369146,6142499.125477515&floor=3
    http://localhost:8000/en/indrz/api/v1/directions/poi-id=27&xyz=1826685.08369146,6142499.125477515&floor=3&reversed=true

    """

    def get(self, request, space_id, xyz, reversed=False, route_type=0):
        """

        :param reversed_dir: boolean to set the direction of route query to allow routing
        from xyz to a space-id
        :param request:
        :param start_poi_id: unique single poi id value, integer
        :param end_xyz: end coordinate pair  x,y  ex) 1826685.08369146,6142499.125477515
        :param z_floor: integer value used to create the z value of xyz coordinate
        :param route_type: 0 for shortest route, 1 for barrierfree route ie no stairs
        :return: GeoJson route from poi id to xyz coordinate

        Usage:   /api/v1/directions/space-id=12764&xyz=1822036.251214,6140092.37464,5&reversed=false&type=0
        """

        start_space_id = int(space_id.split("=")[1])
        xyz_str = xyz.split('=')[1]
        x_end_coord = float(xyz_str.split(",")[0])
        y_end_coord = float(xyz_str.split(",")[1])
        z_end_floor = float(xyz_str.split(",")[2])

        r_type = 0
        if isinstance(route_type, str):
            if route_type.endswith('1'):
                r_type = 1
            if route_type.endswith('0'):
                r_type = 0
        if isinstance(route_type, int):
            r_type = route_type


        try:
            space = BuildingFloorSpace.objects.get(pk=start_space_id)
        except ObjectDoesNotExist:
            return Response({"error": "no space found with given id", "reason": "Sorry no space found"}, status=status.HTTP_200_OK)

        start_node_id = get_room_centroid_node(start_space_id)
        end_node_id = find_closest_network_node(x_end_coord, y_end_coord, z_end_floor)

        if not end_node_id:
            return Response({"error": "n", "reason":"Error no end node"}, status=status.HTTP_200_OK)

        if reversed:
            geojs_fc = run_route(end_node_id, start_node_id, r_type)
        else:
            geojs_fc = run_route(start_node_id, end_node_id, r_type)

        if "error" in geojs_fc:
            return Response(geojs_fc, status=status.HTTP_200_OK)
        else:
            geojs_fc['route_info']['start_name'] = space.room_code
            geojs_fc['route_info']['end_name'] = xyz_str

            if reversed:
                geojs_fc['route_info']['start_name'] = xyz_str
                geojs_fc['route_info']['end_name'] = space.room_code

            return Response(geojs_fc, status=status.HTTP_200_OK)



class RouteSpaceToXyzV0(RouteSpaceToXyz):
    pass


class RouteXyzToXyz(APIView):
    """

        :param request:
        :param start_xyz: unique coordinate pair x,y,z  all as floats
        :param end_xyz: end coordinate pair  x,y,z all as floats
        :param route_type: 0 for shortest route, 1 for barrierfree route ie no stairs
        :return: GeoJson route from xyz id to xyz coordinate

        Usage:   /api/v1/directions/start_xyz=1234.34,2345.45,3.0&end_xyz=456.34,6789.45,2.0&type=0

    """

    def get(self, request, start_xyz, end_xyz, reversed=False, route_type=0):
        """
        :param request:
        :param start_xyz: unique coordinate pair x,y,z  all as floats
        :param end_xyz: end coordinate pair  x,y,z all as floats
        :param route_type: 0 for shortest route, 1 for barrierfree route ie no stairs
        :return: GeoJson route from xyz id to xyz coordinate

        Usage:   /api/v1/directions/start_xyz=1234.34,2345.45,3.0&end_xyz=456.34,6789.45,2.0&type=0
        """

        start_xyz_coords = start_xyz.split("=")[1]
        x_start_coord = float(start_xyz_coords.split(",")[0])
        y_start_coord = float(start_xyz_coords.split(",")[1])
        z_start_floor = float(start_xyz_coords.split(",")[2])

        end_xyz_coords = end_xyz.split('=')[1]
        x_end_coord = float(end_xyz_coords.split(",")[0])
        y_end_coord = float(end_xyz_coords.split(",")[1])
        z_end_floor = float(end_xyz_coords.split(",")[2])

        if start_xyz_coords == end_xyz_coords:
            return Response({"error": "route xyz to xyz", "reason": "Sorry, the xyz start and end locations are the same" }, status=status.HTTP_200_OK)

        r_type = 0
        if isinstance(route_type, str):
            if route_type.endswith('1'):
                r_type = 1
            if route_type.endswith('0'):
                r_type = 0
        if isinstance(route_type, int):
            r_type = route_type

        start_node_id = find_closest_network_node(x_start_coord, y_start_coord, z_start_floor)
        end_node_id = find_closest_network_node(x_end_coord, y_end_coord, z_end_floor)

        if start_xyz_coords is not None and end_node_id is not None:

            geojs_fc = run_route(start_node_id, end_node_id, r_type)
            if reversed:
                geojs_fc = run_route(end_node_id, start_node_id, r_type)

            if "error" in geojs_fc.keys():
                return Response(geojs_fc, status=status.HTTP_200_OK)
            else:

                geojs_fc['route_info']['start_name'] = start_xyz_coords
                geojs_fc['route_info']['end_name'] = end_xyz_coords
                if reversed:
                    geojs_fc['route_info']['start_name'] = end_xyz_coords
                    geojs_fc['route_info']['end_name'] = start_xyz_coords

                return Response(geojs_fc, status=status.HTTP_200_OK)
        else:
            return Response({"error": "no routing node found on network"}, status=status.HTTP_400_BAD_REQUEST)


class RouteSpaceToPoi(APIView):
    """
        :param request:
        :param space_id: unique space id
        :param poi_id: unique poi id
        :param reversed: boolean to set the direction of route query to allow routing
        :param route_type: 0 for normal route, 1 for barrierfree route ie no stairs


        Usage:   /api/v1/directions/space=1234&poi=456&reversed=false&type=0

    """

    def get(self, request, space_id, poi_id, reversed=False, route_type=0):
        """
        :param request:
        :param space_id: unique space id
        :param poi_id: unique poi id
        :param reversed: boolean to set the direction of route query to allow routing
        :param route_type: 0 for normal route, 1 for barrierfree route ie no stairs


        Usage:   /api/v1/directions/space=1234&poi=456&reversed=false&type=0
        """

        start_space_id = int(space_id.split("=")[1])
        end_poi_id = int(poi_id.split("=")[1])
        lang_code = get_language_from_request(request)

        r_type = 0
        if isinstance(route_type, str):
            if route_type.endswith('1'):
                r_type = 1
            if route_type.endswith('0'):
                r_type = 0
        if isinstance(route_type, int):
            r_type = route_type


        try:
            start_space = BuildingFloorSpace.objects.get(pk=start_space_id)

            center_geom = start_space.geom.centroid

            x_coord = float(center_geom.x)
            y_coord = float(center_geom.y)

            start_node_id = find_closest_network_node(x_coord, y_coord, start_space.floor_num)

        except ObjectDoesNotExist:
            return Response({"error": "no space found with given id", "reason": "Sorry no space found"}, status=status.HTTP_200_OK)

        try:
            end_poi = Poi.objects.get(pk=end_poi_id)
            end_node_id = find_closest_network_node(end_poi.geom.coords[0][0], end_poi.geom.coords[0][1],
                                                    end_poi.floor_num)
        except ObjectDoesNotExist:
            return Response({"error": "no poi found with given id", "reason": "Sorry no POI found"}, status=status.HTTP_200_OK)

        geojs_fc = run_route(start_node_id, end_node_id, r_type)
        if reversed:
            geojs_fc = run_route(end_node_id, start_node_id, r_type)

        if "error" in geojs_fc:
            return Response(geojs_fc, status=status.HTTP_200_OK)
        else:
            geojs_fc['route_info']['start_name'] = start_space.short_name
            geojs_fc['route_info']['end_name'] = end_poi.name

            if reversed:
                geojs_fc['route_info']['start_name'] = end_poi.name
                geojs_fc['route_info']['end_name'] = start_space.short_name

            return Response(geojs_fc, status=status.HTTP_200_OK)


class RouteSpaceToSpace(APIView):
    """
        :param request:
        :param space_id: unique space id
        :param poi_id: unique poi id
        :param reversed: boolean to set the direction of route query to allow routing
        :param route_type: 0 for normal route, 1 for barrierfree route ie no stairs


        Usage:   /api/v1/directions/space=1234&poi=456&reversed=false&type=0

    """

    def get(self, request, start_space_id, end_space_id, reversed=False, route_type=0):
        """
        :param request:
        :param space_id: unique space id
        :param poi_id: unique poi id
        :param reversed: boolean to set the direction of route query to allow routing
        :param route_type: 0 for normal route, 1 for barrierfree route ie no stairs


        Usage:   /api/v1/directions/space=1234&space=456&reversed=false&type=0
        """

        start_space_int = int(start_space_id.split("=")[1])
        end_space_id_int = int(end_space_id.split("=")[1])

        if start_space_int == end_space_id_int:
            return Response({"error": "route space id to space id", "reason": "Sorry, the start and end locations are the same" }, status=status.HTTP_200_OK)

        print(start_space_id, end_space_id)
        lang_code = get_language_from_request(request)

        r_type = 0
        if isinstance(route_type, str):
            if route_type.endswith('1'):
                r_type = 1
            if route_type.endswith('0'):
                r_type = 0
        if isinstance(route_type, int):
            r_type = route_type


        try:
            start_space = BuildingFloorSpace.objects.get(pk=start_space_int)
            center_geom = start_space.geom.centroid

            x_coord = float(center_geom.x)
            y_coord = float(center_geom.y)

            start_node_id = find_closest_network_node(x_coord, y_coord, start_space.floor_num)

        except ObjectDoesNotExist:
            return Response({"error": "no space found with given id", "reason": "Sorry no space found"}, status=status.HTTP_200_OK)

        try:
            end_space = BuildingFloorSpace.objects.get(pk=end_space_id_int)
            end_center_geom = end_space.geom.centroid

            x_coord_end = float(end_center_geom.x)
            y_coord_end = float(end_center_geom.y)

            end_node_id = find_closest_network_node(x_coord_end, y_coord_end, end_space.floor_num)
        except ObjectDoesNotExist:
            return Response({"error": "no poi found with given id", "reason": "Sorry no POI found"}, status=status.HTTP_200_OK)


        if reversed:
            geojs_fc = run_route(end_node_id, start_node_id, r_type)
        else:
            geojs_fc = run_route(start_node_id, end_node_id, r_type)

        if "error" in geojs_fc:
            return Response(geojs_fc, status=status.HTTP_200_OK)
        else:
            geojs_fc['route_info']['start_name'] = start_space.short_name
            geojs_fc['route_info']['end_name'] = end_space.short_name

            if reversed:
                geojs_fc['route_info']['start_name'] = end_space.short_name
                geojs_fc['route_info']['end_name'] = start_space.short_name

            return Response(geojs_fc, status=status.HTTP_200_OK)


@api_view(['GET', ])
def route_to_nearest_poi(request, start_xy, floor, poi_cat_id, reversed, route_type):
    coords = start_xy.split("=")[1]
    x_start_coord = float(coords.split(',')[0])
    y_start_coord = float(coords.split(',')[1])
    start_floor_num = int(floor.split('=')[1])
    poi_cat_id_v = int(poi_cat_id.split("=")[1])
    rev_val = reversed.split("=")[1]
    lang_code = get_language_from_request(request)

    r_type = 0
    if isinstance(route_type, str):
        if route_type.endswith('1'):
            r_type = 1
        if route_type.endswith('0'):
            r_type = 0
    if isinstance(route_type, int):
        r_type = route_type


    startid = find_closest_network_node(x_start_coord, y_start_coord, start_floor_num)

    if not startid:
        return Response({"error": "no poi near xyz coordinate"}, status=status.HTTP_400_BAD_REQUEST)

    cur = connection.cursor()

    # bus = pk 27  underground= 26
    qs_nearest_poi = Poi.objects.filter(category=poi_cat_id_v)

    if qs_nearest_poi:
        dest_nodes = []
        pois_found = []

        for i, res in enumerate(qs_nearest_poi):
            network_node_id = find_closest_network_node(res.geom.coords[0][0], res.geom.coords[0][1], res.floor_num)
            if network_node_id:

                if lang_code == "de":
                    pois_found.append({"result_index": i, 'name': res.name_de, 'floor': res.floor_num, 'id': res.id,
                                       'category': res.category.cat_name_de, 'cat_id': res.category.id,
                                       'network_node_id': network_node_id, 'geometry': loads(res.geom.geojson)})
                else:
                    pois_found.append({"result_index": i, 'name': res.name, 'floor': res.floor_num, 'id': res.id,
                                       'category': res.category.cat_name, 'cat_id': res.category.id,
                                       'network_node_id': network_node_id, 'geometry': loads(res.geom.geojson)})

                dest_nodes.append(network_node_id)
            else:
                return Response({"error": "no network node found close to poi", "reason": "Sorry no network found close to POI"}, status=status.HTTP_200_OK)

        pgr_query = """SELECT end_vid, sum(cost) as distance_to_poi
            FROM pgr_dijkstra(
                'SELECT id, source, target, cost FROM geodata.networklines_3857',
                {start_node_id}, ARRAY{poi_ids},FALSE
                -- 2, ARRAY[1077, 1255],
                 )
            GROUP BY end_vid
            ORDER BY distance_to_poi asc
            LIMIT 1;""".format(start_node_id=startid, poi_ids=dest_nodes)

        cur.execute(pgr_query)
        res = cur.fetchall()

        node_id_closest_poi = res[0][0]

        poi_data = OrderedDict()

        for x in pois_found:
            if node_id_closest_poi == x['network_node_id']:
                closest_poi = x
                poi_data['id'] = x['id']
                poi_data['name'] = x['name']
                poi_data['floor'] = x['floor']
                poi_data['geometry'] = x['geometry']['coordinates'][0]
                poi_data['category'] = x['category']
                poi_data['category-id'] = x['cat_id']

        if rev_val == 'true':
            geojs_fc = run_route(node_id_closest_poi, startid, r_type)
        else:
            geojs_fc = run_route(startid, node_id_closest_poi, r_type)

        if "error" in geojs_fc:
            return Response({"error": geojs_fc}, status=status.HTTP_200_OK)
        else:
            geojs_fc['route_info']['start_name'] = ""
            geojs_fc['route_info']['mid_name'] = ""
            geojs_fc['route_info']['poi_info'] = poi_data

            start_coords = {'coordinates': [x_start_coord, y_start_coord], 'type': 'Point'}

            start_name = ""
            end_name = poi_data['name']
            poi_floor = poi_data['floor']
            poi_geom = poi_data['geometry']

            if rev_val == "false":
                marks = create_route_markers(start_coords, poi_geom, start_floor_num, poi_floor, start_name, end_name)
            else:
                marks = create_route_markers(poi_geom, start_coords, poi_floor, start_floor_num, end_name, start_name)

            geojs_fc['route_info']['route_markers'] = marks

            # geojs_fc.update({'route_info':[{'destination':closest_poi},{'start': 'work in progress'},{"name": end_name}]})

            return Response(geojs_fc)
    else:
        return Response({"error": "no Pois with that poi_cat_id found", "reason":"Sorry no POI's with that category found"}, status=status.HTTP_200_OK)


def create_substring_line(coords, node_id, nearest_edge_target_id, nearest_edge_source_id, edge_line_geom, foxy=False):
    sql = ''
    if node_id == nearest_edge_target_id or foxy == True:
        # substring('geom', 0.8, 1) # 1 represents the end of the line
        sql = """(SELECT ST_AsGeoJSON(ST_LineSubstring('{geom}', ST_LineLocatePoint('{geom}',ST_SetSRID(ST_MakePoint{xyz},3857)), 1)))""".format(
            xyz=coords, geom=edge_line_geom)

    elif node_id == nearest_edge_source_id:
        # substring('geom', 0, 0.8)  # 0 represents the start of the line
        sql = """(SELECT ST_AsGeoJSON(ST_LineSubstring('{geom}', 0, ST_LineLocatePoint('{geom}',ST_SetSRID(ST_MakePoint{xyz},3857)))))""".format(
            xyz=coords, geom=edge_line_geom)
    else:
        # substring('geom', 0, 0.8)  # 0 represents the start of the line
        sql = """(SELECT ST_AsGeoJSON(ST_LineSubstring('{geom}', 0, ST_LineLocatePoint('{geom}',ST_SetSRID(ST_MakePoint{xyz},3857)))))""".format(
            xyz=coords, geom=edge_line_geom)

    cur = connection.cursor()
    cur.execute(sql)

    res = cur.fetchall()

    return res

def split_route(route_segments, start_node_id, end_node_id, coord_data):
    if not route_segments:
        return None  # dead at start

    start_coords = tuple(coord_data[0])
    end_coords = tuple(coord_data[1])

    last_sequence_num = route_segments[-1]
    seq_ids = [1, last_sequence_num]

    #####   find nearest start and end edge  ##################

    nearest_start_edge = nearest_edge(start_coords, 'start')
    nearest_end_edge = nearest_edge(end_coords, 'end')

    nearest_start_edge_id = nearest_start_edge[0]
    nearest_start_edge_source_id = nearest_start_edge[3]
    nearest_start_edge_target_id = nearest_start_edge[4]
    start_geom = nearest_start_edge[1]
    start_edge_nodes = (nearest_start_edge_source_id, nearest_start_edge_target_id)

    nearest_end_edge_id = nearest_end_edge[0]
    nearest_end_edge_source_id = nearest_end_edge[3]
    nearest_end_edge_target_id = nearest_end_edge[4]
    end_geom = nearest_end_edge[1]
    end_edge_nodes = (nearest_end_edge_source_id, nearest_end_edge_target_id)

    ################ create new start or end linestring as substring query

    new_start_geom = create_substring_line(start_coords, start_node_id, nearest_start_edge_target_id,
                                           nearest_start_edge_source_id, start_geom)
    new_end_geom = create_substring_line(end_coords, end_node_id, nearest_end_edge_target_id,
                                         nearest_end_edge_source_id,
                                         end_geom)

    first_last_edges = [{"position": "start", "edge-data": nearest_start_edge},
                        {"position": "end", "edge-data": nearest_end_edge}]

    ################ create features  ##########################
    route_result = []
    edge_ids = []
    node_ids = []
    sequence_ids = []

    last_sequence_num = route_segments[-1]
    seq_ids = [1, last_sequence_num]

    for segment in route_segments:
        seg_length = segment[4]  # length of segment
        layer_level = segment[6]  # floor number
        seg_type = segment[7]
        seg_node_id = segment[2]
        seq_sequence = segment[0]
        edge_id = segment[1]
        geojs = segment[8]  # geojson coordinates

        if seq_sequence == 1:

            if set(start_edge_nodes).issubset(set(node_ids)):
                foobar = create_substring_line(start_coords, start_node_id, nearest_start_edge_target_id,
                                               nearest_start_edge_source_id, start_geom, foxy=True)

                geojs_start_geom = loads(foobar[0][0], object_pairs_hook=OrderedDict)  # load string to geom
                geojs_start_feat = Feature(geometry=geojs_start_geom,
                                           properties={'floor': layer_level,
                                                       'segment_length': seg_length,
                                                       'network_type': seg_type,
                                                       'seg_node_id': seg_node_id,
                                                       'sequence': seq_sequence}
                                           )
                route_result.insert(0, geojs_start_feat)

            else:
                geojs_start_geom = loads(new_start_geom[0][0], object_pairs_hook=OrderedDict)  # load string to geom
                geojs_start_feat = Feature(geometry=geojs_start_geom,
                                           properties={'floor': layer_level,
                                                       'segment_length': seg_length,
                                                       'network_type': seg_type,
                                                       'seg_node_id': seg_node_id,
                                                       'sequence': seq_sequence}
                                           )

                route_result.insert(0, geojs_start_feat)

        elif seq_sequence == last_sequence_num:
            # replace with split line

            geojs_end_geom = loads(new_end_geom[0][0], object_pairs_hook=OrderedDict)  # load string to geom
            geojs_end_feat = Feature(geometry=geojs_end_geom,
                                     properties={'floor': layer_level,
                                                 'segment_length': seg_length,
                                                 'network_type': seg_type,
                                                 'seg_node_id': seg_node_id,
                                                 'sequence': seq_sequence}
                                     )
            route_result.append(geojs_end_feat)

        geojs_geom = loads(geojs, object_pairs_hook=OrderedDict)  # load string to geom
        geojs_feat = Feature(geometry=geojs_geom,
                             properties={'floor': layer_level,
                                         'segment_length': seg_length,
                                         'network_type': seg_type,
                                         'seg_node_id': seg_node_id,
                                         'sequence': seq_sequence}
                             )
        route_result.append(geojs_feat)

        edge_ids.append(edge_id)
        node_ids.append(seg_node_id)
        sequence_ids.append(seq_sequence)

    for edge in first_last_edges:

        id = edge['edge-data'][0]
        edge_geom = edge['edge-data'][8]

        if id in edge_ids:
            # do split line at coord on edge is already part of the route
            pass

        else:

            # edge id is not in the list of edges so add it
            geojs_start_geom = loads(new_start_geom[0][0], object_pairs_hook=OrderedDict)  # load string to geom
            geojs_start_feat = Feature(geometry=geojs_start_geom,
                                       properties={'floor': edge['edge-data'][2],
                                                   'segment_length': edge['edge-data'][6],
                                                   'network_type': edge['edge-data'][7],
                                                   'seg_node_id': edge['edge-data'][0],
                                                   'sequence': edge['position']}
                                       )

            geojs_end_geom = loads(new_end_geom[0][0], object_pairs_hook=OrderedDict)  # load string to geom
            geojs_end_feat = Feature(geometry=geojs_end_geom,
                                     properties={'floor': edge['edge-data'][2],
                                                 'segment_length': edge['edge-data'][6],
                                                 'network_type': edge['edge-data'][7],
                                                 'seg_node_id': edge['edge-data'][0],
                                                 'sequence': edge['position']}
                                     )

            if edge['position'] == 'start':
                # edge_ids.insert(0, edge['edge-data'][0])
                route_result.insert(0, geojs_start_feat)  # insert at first position of list

            if edge['position'] == 'end':
                # edge_ids.append(edge['edge-data'][0])
                route_result.append(geojs_end_feat)

    if route_result:
        return route_result
    else:
        return None


def run_route(start_node_id, end_node_id, route_type=0, mid_node_id=None, coord_data=None):
    """

    :param start_node_id:
    :param end_node_id:
    :param route_type:
    :param route_options: a dictionary
    :return:
    """

    # TODO add route options dictionary
    # TODO add parameter to function   route_options=None

    # sample dictionary of options
    # route_options = {'route_types': {
    #     'standard_route': 1,
    #     'barrierfree route': 2,
    #     'indoor_only_prefered': 3,
    #     'fastest': 4
    # },
    #     'route_logic': {
    #         'force_route_through_location': True
    #     }
    # }


    # check if route_type is an integer
    if isinstance(route_type, int):
        pass
    if isinstance(route_type, str):
        if route_type.endswith("0"):
            route_type = 0
        if route_type.endswith("1"):
            route_type = 1

    cur = connection.cursor()

    base_route_q = """SELECT id, source, target, cost, reverse_cost, floor_name FROM geodata.networklines_3857"""

    # default type is "0"
    barrierfree_q = "WHERE 1=1"

    if route_type == 1:
        # exclude all networklines of type stairs
        barrierfree_q = "WHERE network_type not in (1,11)" # 1 = stairs floor change, 11 = stairs no floor change

    route_query = "SELECT id, source, target, cost, reverse_cost, floor_name FROM geodata.networklines_3857"

    route_node_array = [start_node_id, end_node_id]

    routing_query = """
        SELECT seq, id, node, edge,
            ST_Length(st_transform(geom,4326), TRUE ) AS cost, agg_cost, floor, network_type,
            ST_AsGeoJSON(geom) AS geoj, floor_name
        FROM pgr_dijkstra( '{sql_query} {type}',{start_node}, {end_node}) AS dij_route

          JOIN geodata.networklines_3857 AS input_network
          ON dij_route.edge = input_network.id ;""".format(sql_query=route_query, type=barrierfree_q,
                                                           start_node=start_node_id, end_node=end_node_id)

    if mid_node_id:
        route_node_array = [start_node_id, mid_node_id, end_node_id]
        if route_node_array:
            routing_query = """
                SELECT seq, id, node, edge,
                    ST_Length(st_transform(geom,4326), TRUE ) AS cost, agg_cost, floor, network_type,
                    ST_AsGeoJSON(geom) AS geoj, floor_name
                FROM pgr_dijkstraVia( '{normal} {type}', ARRAY{nodes}) AS dij_route
    
                  JOIN geodata.networklines_3857 AS input_network
                  ON dij_route.edge = input_network.id ;""".format(normal=route_query, type=barrierfree_q,
                                                                   nodes=route_node_array,
                                                                   start_node=start_node_id, end_node=end_node_id)
        else:
            return {"error": "no mid node id", "reason": "mid node id is None"}

    # run our shortest path query
    if start_node_id or end_node_id:
        if start_node_id != end_node_id:
            # cur.execute(routing_query, (start_node_id, end_node_id))
            # cur.execute(routing_query)
            try:
                cur.execute(routing_query)
                route_simple = cur.fetchall()
            except Exception as e:
                # Handle the error
                logger.info("routing query failed here is the query \n " + routing_query + " error " + str(e))
                return {"error": "no route", "reason": "Sorry, no matching start end nodes found"}
        else:
            logger.info("same ids start end node \n " + str(start_node_id) + " " + str(end_node_id))
            return {"error": "same ids", "reason": "Sorry, the start node is equal to end node no routes between equal locations"}
    else:
        logger.info("start or end node is None" + str(start_node_id))
        return {"error": "start or end node is none", "reason": f"Sorry, start node is {str(start_node_id)} END node is {str(end_node_id)}"}


    route_info = calc_distance_walktime(route_simple)
    route_result = []

    if "error" in route_info.keys():
        return {"error": "no route", "reason": "Sorry no route found",
                "route_info_res": f"{route_info}"}
    else:

        if (coord_data):
            route_result = split_route(route_simple, start_node_id, end_node_id, coord_data)

        # loop over each segment in the result route segments
        # create the list of our new GeoJSON
        for segment in route_simple:
            seg_length = segment[4]  # length of segment
            layer_level = segment[6]  # floor number
            seg_type = segment[7]
            seg_node_id = segment[2]
            seq_sequence = segment[0]
            geojs = segment[8]  # geojson coordinates
            floor_name = segment[9]
            # geojs = big_test[0]
            geojs_geom = loads(geojs, object_pairs_hook=OrderedDict)  # load string to geom
            geojs_feat = Feature(geometry=geojs_geom,
                                 properties={'floor': layer_level,
                                             'floor_name': floor_name,
                                             'segment_length': seg_length,
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
def create_route_from_id(request, start_room_id, end_room_id, route_type, front_office_id=None):
    """
    Generate a GeoJSON route from space id to space id
    :param request: GET or POST request
    :param start_room_id: an integer space id
    :param end_room_id: an integer space id
    :param route_type: an integer route type
    :param front_office_id: an integer of space id for the front office
    :return: a GeoJSON linestring of the route
    """

    if request.method == 'GET' or request.method == 'POST':

        start_room = int(start_room_id.split("=")[1])
        end_room = int(end_room_id.split("=")[1])

        r_type = 0
        if isinstance(route_type, str):
            if route_type.endswith('1'):
                r_type = 1
            if route_type.endswith('0'):
                r_type = 0
        if isinstance(route_type, int):
            r_type = route_type



        start_node_id = get_room_centroid_node(start_room)
        end_node_id = get_room_centroid_node(end_room)

        start_qs = get_object_or_404(BuildingFloorSpace, pk=start_room)
        end_qs = get_object_or_404(BuildingFloorSpace, pk=end_room)

        try:
            if start_node_id and end_node_id:
                if start_node_id == end_node_id:
                    return Response({'error': 'start and end node cannot be the same'}, status.HTTP_400_BAD_REQUEST)
                else:
                    if front_office_id:
                        foid = int(front_office_id.split("=")[1])
                        front_office_node = get_room_centroid_node(foid)
                        res = run_route(start_node_id, end_node_id, r_type, mid_node_id=front_office_node)
                    else:
                        res = run_route(start_node_id, end_node_id, r_type)
                    if "error" not in res.keys():
                        res['route_info']['start_name'] = start_qs.room_code
                        res['route_info']['end_name'] = end_qs.room_code
                        return Response(res)
                    else:
                        return Response({'error': f'no route found in create route {res}', "reason":"Sorry no route found"}, status=status.HTTP_200_OK)
            else:
                # if "error" in start_node_id or "error" in end_node_id:
                return Response({'error': 'route by id is not sending response', "reason":"Sorry no route found"}, status=status.HTTP_200_OK)
        except:
            logger.info(traceback.format_exc())
            return Response({'error': 'running route function failed', "reason":"Sorry no route found"}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'post or get', "reason":"Sorry no route found"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def route_space_id_and_poi_id(request, space_id, poi_id, route_type, reversed_direction=False):
    """
    Generate a GeoJSON route between a space-id and a poi-id
    :param request: GET or POST request
    :param space_id: an integer of internal space id
    :param poi_id: an integer of internal poi-id
    :param route_type: an integer room type either 0 standard or 1 barrierefree
    :param reversed_direction: route from space-id to poi-id if true, default route from poi-id to space-id
    :return: a GeoJSON linestring of the route
    """

    if request.method == 'GET' or request.method == 'POST':

        end_room_id = int(space_id.split("=")[1])
        poi_id_value = int(poi_id.split("=")[1])

        r_type = 0
        if isinstance(route_type, str):
            if route_type.endswith('1'):
                r_type = 1
            if route_type.endswith('0'):
                r_type = 0
        if isinstance(route_type, int):
            r_type = route_type

        end_node_id = get_room_centroid_node(end_room_id)

        try:
            poi = Poi.objects.get(pk=poi_id_value)
        except ObjectDoesNotExist:
            return Response({"error": "no poi found with given id", "reason":"Sorry no POI found"}, status=status.HTTP_200_OK)

        x_coord_poi = poi.geom.coords[0][0]
        y_coord_poi =poi.geom.coords[0][1]
        poi_floor = poi.floor_num

        space = BuildingFloorSpace.objects.get(pk=end_room_id)


        start_node_id = find_closest_network_node(x_coord_poi, y_coord_poi, poi_floor)

        if not start_node_id:
            return Response({"error": "no start_node_id ", "reason":"Sorry no start found"}, status=status.HTTP_200_OK)

        if reversed_direction:
            res = run_route(end_node_id, start_node_id, r_type)
            if "error" in res:
                return Response({"error": res, "reason":f"Sorry {res}"}, status=status.HTTP_200_OK)
            else:
                res['route_info']['start_name'] = space.room_code
                res['route_info']['end_name'] = poi.name
                return Response(res)
        else:
            res = run_route(start_node_id, end_node_id, route_type=r_type)
            if "error" in res:
                return Response({"error": res, "reason":f"Sorry {res}"}, status=status.HTTP_200_OK)
            else:
                res['route_info']['start_name'] = poi.name
                res['route_info']['end_name'] = space.room_code
                return Response(res)
    else:
        return Response({'error': 'either no JSON or no key params in your JSON', "reason":f"Sorry json error"}, status=status.HTTP_200_OK)



def get_features(FeatureCollection):
    props_list = []
    for feature in FeatureCollection:
        props_list.append(feature['properties'])

    return props_list


def create_mid_point(feature):
    if feature['features'][0]['properties']['frontoffice']:
        cur = connection.cursor()

        # fo = front office
        fo_aks = feature['features'][0]['properties']['frontoffice']['location']
        fo_name = feature['features'][0]['properties']['frontoffice']['name']
        fo_floor_num = feature['features'][0]['properties']['frontoffice']['floor_num']
        fo_coords = feature['features'][0]['properties']['frontoffice']['geom']['coordinates']

        mid_query = """SELECT id, external_id, search_string FROM geodata.search_index_v
                          WHERE search_string LIKE '%{0}%'
                          OR external_id = '{0}'
                          ORDER BY length(search_string) LIMIT 1""".format(fo_aks)

        # logger.debug('**************print END  query' + str(end_query))
        cur.execute(mid_query)

        mid_id_list = cur.fetchone()
        mid_id_value = mid_id_list[0]
        # mid_name = _("Please first visit the {name} front office located at room number {room_code}".format(name=fo_name,
        #                                                                      room_code=mid_id_list[2]))
        mid_name = "{name} ({roomcode})".format(name=fo_name, roomcode=mid_id_list[2])
        mid_id = get_room_centroid_node(mid_id_value)

        if isinstance(mid_id, int):
            return {"id": mid_id, "name": mid_name, "coords": fo_coords, "floor": fo_floor_num, 'fo-name': fo_name}
        else:
            return None
    else:
        return None


@api_view(['GET', 'POST'])
def create_route_from_search(request, start_term, end_term, route_type=0):
    """
    Generate a GeoJSON route from room number
    to room number
    :param request: GET or POST request
    :param building_id: buiilding id as integer
    :param start_term: a text string as search term
    :param end_term: a text string as search term
    :param route_type: an integer room type
    :return: a GeoJSON linestring of the route
    """

    r_type = 0
    if isinstance(route_type, str):
        if route_type.endswith('1'):
            r_type = 1
        if route_type.endswith('0'):
            r_type = 0
    if isinstance(route_type, int):
        r_type = route_type


    if request.method == 'GET' or request.method == 'POST':

        lang_code = get_language_from_request(request)

        start_room = start_term.split("=")[1]
        end_room = end_term.split("=")[1]

        mid_id = None
        mid_name = ""
        mid_coords = None
        mid_point_info = None
        start_aks = ""

        res_start = search_only(start_room, lang_code)
        res_end = search_only(end_room, lang_code)

        if res_start and res_end:

            fx1 = res_start
            fx2 = res_end

            if 'aks_nummer' in fx1['features'][0]['properties']:
                if fx1['features'][0]['properties']['aks_nummer'] != "":
                    start_aks = fx1['features'][0]['properties']['aks_nummer']
            else:
                start_aks = None

            if 'frontoffice' in fx2['features'][0]['properties']:

                mid_point_info = create_mid_point(fx2)

                if mid_point_info:
                    mid_name = mid_point_info['name']
                    mid_id = mid_point_info['id']
                    mid_coords = mid_point_info['coords']
                    fo_name = mid_point_info['fo-name']

            if 'centerGeometry' in fx1['features'][0]['properties']:

                if fx1['features'][0]['properties']['centerGeometry']['type'] == "MultiPoint":
                    x_start_coord = fx1['features'][0]['properties']['centerGeometry']['coordinates'][0][0]
                    y_start_coord = fx1['features'][0]['properties']['centerGeometry']['coordinates'][0][1]
                else:
                    x_start_coord = fx1['features'][0]['properties']['centerGeometry']['coordinates'][0]
                    y_start_coord = fx1['features'][0]['properties']['centerGeometry']['coordinates'][1]

                # x_start_coord = fx1['features'][0]['properties']['centerGeometry']['coordinates'][0][0]
                # y_start_coord = fx1['features'][0]['properties']['centerGeometry']['coordinates'][0][1]
                start_floor = fx1['features'][0]['properties']['floor_num']

                start_node_id = find_closest_network_node(x_start_coord, y_start_coord, start_floor)

                if 'centerGeometry' in fx2['features'][0]['properties']:

                    if fx2['features'][0]['properties']['centerGeometry']['type'] == "MultiPoint":
                        x_end_coord = fx2['features'][0]['properties']['centerGeometry']['coordinates'][0][0]
                        y_end_coord = fx2['features'][0]['properties']['centerGeometry']['coordinates'][0][1]
                    else:
                        x_end_coord = fx2['features'][0]['properties']['centerGeometry']['coordinates'][0]
                        y_end_coord = fx2['features'][0]['properties']['centerGeometry']['coordinates'][1]

                    # x_end_coord = fx2['features'][0]['properties']['centerGeometry']['coordinates'][0]
                    # y_end_coord = fx2['features'][0]['properties']['centerGeometry']['coordinates'][1]
                    end_floor = fx2['features'][0]['properties']['floor_num']

                    start_coords = fx1['features'][0]['properties']['centerGeometry']
                    end_coords = fx2['features'][0]['properties']['centerGeometry']

                    route_markers_geojs = create_route_markers(start_coords, end_coords, start_floor, end_floor,
                                                               start_room, end_room, mid_point_info)

                    end_node_id = find_closest_network_node(x_end_coord, y_end_coord, end_floor)

                    start_data = [x_start_coord, y_start_coord, start_floor]
                    end_data = [x_end_coord, y_end_coord, end_floor]

                    coord_data = [start_data, end_data]

                    # TODO fix split route function it inserts points into route for some reason!
                    # Removed coord_data so route is not split
                    # there is an error in split route function it is inserting a POINT in the route and then
                    # things fail
                    # res = run_route(start_node_id, end_node_id, route_type_val, mid_node_id=mid_id, coord_data=coord_data)
                    res = run_route(start_node_id, end_node_id, r_type, mid_node_id=mid_id)

                    if "error" in res:
                        return Response({"error": res}, status=status.HTTP_200_OK)
                    else:
                        res['route_info']['start_name'] = start_room
                        res['route_info']['mid_name'] = mid_name
                        res['route_info']['end_name'] = end_room
                        res['route_info']['route_markers'] = route_markers_geojs

                        try:
                            return Response(res)
                        except:
                            logger.info("error exporting to json model: " + str(res))
                            logger.info(traceback.format_exc())
                            return Response({'error': 'either no JSON or no key params in your JSON', "reason":f"Sorry json error"}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'no center geometry', "reason":f"Sorry no center found"}, status=status.HTTP_200_OK)
        else:
            logger.info(traceback.format_exc())
            logger.debug("what is wrong")
            return Response({'error': traceback.format_exc(), "reason":"Sorry no result found"})
    else:
        return Response({'error': 'no data found', "reason":f"Sorry no data found"}, status=status.HTTP_200_OK)



