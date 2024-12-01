import logging
import traceback
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist

from buildings.models import BuildingFloorSpace

logger = logging.getLogger(__name__)
from django.db import connection
from poi_manager.models import Poi
from geojson import loads, Feature, MultiPoint, Point


def find_closest_poi(coordinates, floor, poi_cat_id, lang_code):
    x_start_coord = float(coordinates.split(',')[0])
    y_start_coord = float(coordinates.split(',')[1])
    start_floor_num = floor
    poi_cat_id_v = poi_cat_id

    startid = find_closest_network_node(x_start_coord, y_start_coord, start_floor_num)

    if not startid:
        return {"error": "startid is none"}


    cur = connection.cursor()

    qs_nearest_poi = Poi.objects.filter(category=poi_cat_id_v)

    if qs_nearest_poi:
        dest_nodes = []
        pois_found = []

        for i, res in enumerate(qs_nearest_poi):
            network_node_id = find_closest_network_node(res.geom.coords[0][0], res.geom.coords[0][1], res.floor_num)
            if network_node_id:
                if lang_code == "de":
                    pois_found.append({"result_index": i, 'name': res.name_de, 'floor': res.floor_num, 'id': res.id,
                                       'category': res.category.cat_name_de,
                                       'cat_id': res.category.id,
                                       'icon': res.icon,
                                       'network_node_id': network_node_id, 'geometry': loads(res.geom.geojson)})
                else:
                    pois_found.append({"result_index": i, 'name': res.name, 'floor': res.floor_num, 'id': res.id,
                                       'category': res.category.cat_name, 'cat_id': res.category.id, 'icon': res.icon,
                                       'network_node_id': network_node_id, 'geometry': loads(res.geom.geojson)})

                dest_nodes.append(network_node_id)

            else:
                continue
                # return Response({"error": "no network node found close to poi"}, status=status.HTTP_400_BAD_REQUEST)

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

        if res:
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

            return poi_data
        else:
            return {"error": "res empty, no routes to poi"}
    else:
        return {"error": f"did not receive any entrance points from POI data in category {poi_cat_id_v}"}


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
    speed_map = {"stairs": 1.2, "elevator": 1.1, "walking": 1.39}
    walk_speed = 0

    for row in rows:

        route_length += row[4]
        # calculate walk time
        if row[5] == 3 or row[5] == 4:  # stairs
            walk_speed = speed_map['stairs']  # meters per second m/s
        elif row[5] == 5 or row[5] == 6:  # elevator
            walk_speed = speed_map['elevator']  # m/s
        else:
            walk_speed = speed_map['walking']  # m/s

        walk_time += (row[4] / walk_speed)

    length_format = "%.2f" % route_length
    real_time = format_walk_time(walk_time)

    route_info = {"route_info": {"route_length": length_format, "walk_time": walk_time}}

    if route_length == 0:
        return {"error": "route has length of zero"}
    else:
        return route_info


def format_walk_time(walk_time):
    """
    takes argument: float walkTime in seconds
    returns argument: string time  "xx minutes xx seconds"
    """
    if walk_time > 0.0:
        # return str(int(walk_time / 60.0)) + " minutes " + str(int(round(walk_time % 60))) + " seconds"

        return walk_time
    else:
        return "Walk time is less than zero! something is wrong"


def nearest_edge(xyz_coords, position):
    """

    :param xyz_coords:(1587984.921,5879665.803,2 )
    :return:
    :usage:
    nearest_edge((1587984.921,5879665.803,2 ))
    """
    cur = connection.cursor()
    x_coord = xyz_coords[0]
    y_coord = xyz_coords[1]
    floor = xyz_coords[2]

    # find nearest edge on network within 200 m
    # sql_get_new_start_segment = """SELECT ST_AsGeoJSON(ST_LineSubstring('{edge}', ST_LineLocatePoint('{edge}',ST_SetSRID(ST_MakePoint({x},{y},{z}),3857)), 1)) """.format(edge=first_edge_geom, x=start_coords[0], y=start_coords[1], z=start_coords[2])
    sql_end = """(SELECT ST_AsGeoJSON(ST_LineSubstring(geom, ST_LineLocatePoint(geom,ST_SetSRID(ST_MakePoint({0},{1},{2}),3857)), 1)))""".format(
        x_coord, y_coord, floor)
    sql_start = """(SELECT ST_AsGeoJSON(ST_LineSubstring(geom, 0, ST_LineLocatePoint(geom,ST_SetSRID(ST_MakePoint({0},{1},{2}),3857)))))""".format(
        x_coord, y_coord, floor)
    sql_position = ''

    if position == 'start':
        sql_position = sql_end
    if position == 'end':
        sql_position = sql_start

    query = """ SELECT id as edge,
                geom as geom,
                floor,
                source,
                target,
                ST_3DDistance(geom, ST_PointFromText('POINT({0} {1} {2})', 3857)) as dist,
                ST_Length(geom) as len,
                network_type,
                -- st_lineinterpolatepoint(geom, 0.5), -- returns a point on a line
                -- st_linelocatepoint(line, point) -- returns a float of point location

                '{3}' as lstring
                FROM geodata.networklines_3857
                     ORDER BY dist ASC
                     LIMIT 1;""".format(x_coord, y_coord, floor, sql_position)

    tmp1 = query.replace("'(SELECT", "(SELECT")
    ff = tmp1.replace("))'", "))")
    cur.execute(ff)

    # get the result
    query_result = cur.fetchone()

    # check if result is not empty
    if query_result is not None:
        # get first result in tuple response there is only one

        return query_result
    else:
        logger.debug("query is none check tolerance value of 200")
        return False


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
        ON ST_DWithin(verts.the_geom, pt.geom, 50) and st_Z(verts.the_geom)={2}
        ORDER BY ST_3DDistance(verts.the_geom, pt.geom)
        LIMIT 1;""".format(x_coord, y_coord, floor)

    try:
        cur.execute(query)
    except Exception as e:
        # Handle the error
        logger.error("routing query failed here is the query \n " + query + " error " + str(e))
        return None

    # get the result
    query_result = cur.fetchone()

    # check if result is not empty
    if query_result is not None:
        # get first result in tuple response there is only one
        point_on_networkline = int(query_result[0])
        return point_on_networkline
    else:
        logger.debug("query is none check tolerance value of 200")
        return None


def get_room_centroid_node(space_id):
    '''
    Find the room center point coordinates
    and find the closest route node point
    :param building_id: integer value of building
    :param space_id: internal space id as integer
    :return: Closest route node to submitted room number
    '''


    try:
        qs = BuildingFloorSpace.objects.get(pk=space_id)
    except ObjectDoesNotExist:
        logger.error("error get room center " + str(space_id))
        logger.error(traceback.format_exc())
        return {'error': 'error get room center'}

    center_geom = qs.geom.centroid

    x_coord = float(center_geom.x)
    y_coord = float(center_geom.y)

    space_node_id = find_closest_network_node(x_coord, y_coord, qs.floor_num)
    if space_node_id:
        return space_node_id
    else:
        logger.error("error get room center " + str(space_node_id))
        logger.error(traceback.format_exc())
        return {'error': 'error get room center'}


def create_route_markers(start_coords, end_coords, start_floor, end_floor, start_name, end_name, midpoint=None):
    # markers indicating floor level one per floor
    floor_markers = []

    # indicate where on the route you enter or exit a building
    entrance_markers = []

    # floor change markers such as elevator, stairs, ramp
    floor_change_markers = []

    # markers indicating start, end and optional midpoint destination
    destination_markers = []

    route_markers = []

    s_coords = None
    e_coords = None
    start_feature = None
    end_feature = None

    if start_coords['type'] == "MultiPoint":
        s_coords = start_coords['coordinates']
        start_feature = Feature(geometry=MultiPoint(s_coords),
                                properties={'start': 'start location', 'floor': int(start_floor), 'name': start_name}
                                )
    if start_coords['type'] == "Point":
        s_coords = start_coords['coordinates']
        start_feature = Feature(geometry=Point(s_coords),
                                properties={'start': 'start location', 'floor': int(start_floor), 'name': start_name}
                                )

    if end_coords['type'] == "MultiPoint":
        e_coords = end_coords['coordinates']
        end_feature = Feature(geometry=MultiPoint(e_coords),
                              properties={'end': 'end location', 'floor': int(end_floor), 'name': end_name}
                              )
    if end_coords['type'] == "Point":
        e_coords = end_coords['coordinates']
        end_feature = Feature(geometry=Point(e_coords),
                              properties={'end': 'end location', 'floor': int(end_floor), 'name': end_name}
                              )

    if midpoint:
        mid_feature = Feature(geometry=Point(midpoint['coords']),
                         properties={'mid': 'front office', 'floor': midpoint['floor'], 'name': midpoint['fo-name']}
                         )
        destination_markers.append(mid_feature)


    destination_markers.append(start_feature)
    destination_markers.append(end_feature)

    return destination_markers
