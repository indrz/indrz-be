import os
import psycopg2

from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASSWORD')

con_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass}"
ogr_db_con = f"PG: host={db_host} user={db_user} dbname={db_name} password={db_pass}"


conn = psycopg2.connect(con_string)
cur = conn.cursor()


# sql = """ SELECT ST_AsText(ST_Split(ST_Snap(n.geom, p.geom, 1), p.geom))
#     FROM starting_network n, cut_points_multi p;"""

sql_drop = F"""
                DROP TABLE IF EXISTS geodata.dc_intersections CASCADE;
                DROP TABLE IF EXISTS geodata.dc_union CASCADE;
                DROP TABLE IF EXISTS geodata.dc_segments CASCADE;"""

cur.execute(sql_drop)
conn.commit()


split_lines_query = """ CREATE TABLE geodata.split_network_01
    AS SELECT(ST_Dump(ST_Node(ST_Collect(geom)))).geom AS geom
    FROM routing.routing_networklines_01;
                     """

split_lines_query = """ CREATE TABLE geodata.split_network_01
    AS SELECT(ST_Dump(ST_Node(ST_Collect(geom)))).geom AS geom
    FROM routing.routing_networklines_01;
                     """


s = """--Get a list of all intersections in city
CREATE TABLE geodata.dc_intersections AS 
SELECT DISTINCT (ST_DUMP(ST_INTERSECTION(a.geom, b.geom))).geom AS geom 
FROM routing.routing_networklines_01 a 
INNER JOIN routing.routing_networklines_01 b 
ON ST_INTERSECTS(a.geom,b.geom)
WHERE geometrytype(st_intersection(a.geom,b.geom)) = 'POINT';"""

s2 = "CREATE INDEX ON geodata.dc_intersections USING gist(geom);"

# s3 = """CREATE TABLE geodata.dc_union AS
# SELECT ST_UNION(geom) as geom
# FROM routing.routing_networklines_01;"""
#
# s4 = """CREATE INDEX ON geodata.dc_union USING gist(geom);"""
#
# s5 = """CREATE TABLE geodata.dc_segments AS
# SELECT (ST_DUMP(ST_SPLIT(a.geom,b.ix))).geom
# FROM geodata.dc_union a
# LEFT JOIN geodata.dc_intersections b
# ON ST_INTERSECTS(a.geom, b.ix);"""

snew = """DROP TABLE IF EXISTS geodata.split_01 CASCADE;
CREATE TABLE geodata.split_01 AS SELECT (ST_Dump(ST_Split(n, p))).geom AS geom
FROM (SELECT  n1.geom as n,  p1.ix as p FROM routing.routing_networklines_01 as n1, geodata.dc_intersections as p1) AS foo;"""

snw = """create table geodata.test1 as SELECT ST_Split(ST_Snap(n.geom, p.ix, 1), p.ix) as geom
    FROM routing.routing_networklines_01 as n, geodata.dc_intersections as p;"""




ss = """DROP TABLE IF EXISTS geodata.split_roads CASCADE;
CREATE TABLE geodata.split_roads as
SELECT    
    (ST_Dump(ST_Split(g.geom, blade.geom))).geom As geom,
    generate_series(1,ST_NumGeometries((ST_Split(g.geom, blade.geom)))) as gid
FROM    
    geodata.dc_intersections as blade,
    routing.routing_networklines_01 as g
WHERE
    ST_Intersects(g.geom, blade.geom);
    """


cur.execute(s)
cur.execute(s2)

cur.execute(ss)
# cur.execute(s2)
# cur.execute(s3)
# cur.execute(s4)
# cur.execute(s5)


conn.commit()

# close cursor
cur.close()

# close connection
conn.close()