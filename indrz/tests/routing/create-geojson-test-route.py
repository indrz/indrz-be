# Copyright (C) 2014-2016 Michael Diener <m.diener@gomogi.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from collections import OrderedDict

import psycopg2
import json
from geojson import loads, Feature, FeatureCollection
from dotenv import load_dotenv

load_dotenv(r'C:\Users\mdiener\Dev\pyspace\indrz-tu\indrz\settings\.env')



# connect to DB

db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_pwd = os.getenv('POSTGRES_PASS')
db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')



conn = psycopg2.connect(host=db_host, user=db_user, port=db_port,
                        password=db_pwd, database=db_name)

# create a cursor
cur = conn.cursor()


def nearest_edge(xyz_coords):
    """

    :param xyz_coords:
    :return:
    """
    x_coord = xyz_coords[0]
    y_coord = xyz_coords[1]
    floor = xyz_coords[2]

    # find nearest edge on network within 200 m

    query = """ SELECT id as edge,
        geom,
        floor, source,target,
        ST_3DDistance(geom, ST_PointFromText('POINT({0} {1} {2})', 3857)) as dist
        FROM geodata.networklines_3857
             ORDER BY dist ASC
             LIMIT 1;""".format(x_coord, y_coord, floor)

    cur.execute(query)

    # get the result
    query_result = cur.fetchone()

    # check if result is not empty
    if query_result is not None:
        # get first result in tuple response there is only one

        return query_result
    else:
        print("error")
        return False




start_coords = "1587949.010,879614.590,3"
end_coords = "1587951.563,5879613.595,3"

start_coords_str = start_coords.split(",")
end_coords_str = end_coords.split(",")

start_x = float(start_coords_str[0])
start_y = float(start_coords_str[1])
start_z = int(start_coords_str[2])

end_x = float(end_coords_str[0])
end_y = float(end_coords_str[1])
end_z = int(end_coords_str[2])

# start_x = 1587954.174
# start_y = 5879616.333
# start_z = 1
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

nearest_node_sql = """SELECT
    verts.id AS id
    FROM geodata.networklines_3857_vertices_pgr AS verts
    INNER JOIN
      (SELECT ST_PointFromText('POINT({0} {1} {2})', 3857)AS geom) AS pt
    ON ST_DWithin(verts.the_geom, pt.geom, 50) AND st_Z(verts.the_geom)={2}
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
                                        startX=start_x, startY=start_y, startZ=start_z,
                                        endX=end_x, endY=end_y, endZ=end_z)
print(routing_query)
cur.execute(routing_query)

route_segments = cur.fetchall()

nearest_end_edge = nearest_edge((end_x, end_y, end_z))
print(nearest_end_edge)

first_edge_geom = route_segments[0][10]
last_edge_geom = route_segments[-1][10]

print(route_segments[-1][1])

# returns geometry ST_LineSubstring(geometry a_linestring, float8 startfraction, float8 endfraction);

sql_get_new_start_segment = """ SELECT ST_AsGeoJSON(ST_LineSubstring('{edge}', ST_LineLocatePoint('{edge}', ST_SetSRID(ST_MakePoint({x}, {y}, {z}),3857)), 1)) """.format(
    edge=first_edge_geom, x=start_x, y=start_y, z=start_z)
sql_get_new_end_segment = """ SELECT ST_AsGeoJSON(ST_LineSubstring('{edge}', 0, ST_LineLocatePoint('{edge}', ST_SetSRID(ST_MakePoint({x}, {y}, {z}),3857))))""".format(
    edge=nearest_end_edge[1], x=end_x, y=end_y, z=end_z)

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

n_rsegs.pop(0)
n_rsegs.insert(0, route_segments2)

n_rsegs.pop(-1)
n_rsegs.insert(-1, route_segments3)

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


# define the output folder and GeoJSON file name
output_geojson_route = "test_3d_route.geojson"


# save geojson to a file in our geodata folder
def write_geojson():
    with open(output_geojson_route, "w") as geojs_out:
        geojs_out.write(json.dumps(geojs_fc))


# run the write function to actually create the GeoJSON file
write_geojson()

# clean up and close database curson and connection
cur.close()
conn.close()
