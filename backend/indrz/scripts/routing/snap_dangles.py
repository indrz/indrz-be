import psycopg2
import os

db_user = os.getenv('PG_USER')
db_name = os.getenv('PG_DB')
db_host = os.getenv('PG_HOST')
db_pass = os.getenv('PG_PASS')
db_port = os.getenv('PG_PORT')


con_local = f"dbname=indrztu user=indrztu host=indrz_db password=air port=5432"
con_prod = f"dbname=indrztu user=tu host=tuw-maps.tuwien.ac.at password=air port=5433"


conn = psycopg2.connect(con_local)
cur = conn.cursor()




def fix_geo(tablename):

    s = f"""
    SELECT id, geom FROM {tablename} a
        WHERE NOT EXISTS 
         (SELECT 1 FROM {tablename} b 
          WHERE a.id != b.id
          AND   ST_Intersects(a.geom, b.geom))
      """
    cur.execute(s)
    res = cur.fetchall()

    print(len(res))



    for line in res:
        line_id = line[0]
        line_geom = line[1]

        sql_snap = f"""
        update {tablename} set geom = st_snap('{line_geom}', geom, 0.1) where id = {line_id};
        """
       #  print(sql_snap)

        cur.execute(sql_snap)
    conn.commit()

fix_geo('routing.routing_networklines_eg_noded')

# more_tests = f"""
#
# WITH firststep AS( SELECT id, ST_BOUNDARY(geom) AS boundary
# FROM polygons)
#
# SELECT p.id, ST_Intersection(boundary, geom), o.id
# FROM firststep p
# INNER JOIN othergeoms o ON ST_INTERSECTS(boundary, geom)
#
# UNION
#
# SELECT p.id, ST_SymDifference(boundary, geom), o.id
# FROM firststep p
# INNER JOIN othergeoms o ON ST_INTERSECTS(boundary, geom)
#
# """
#
# # input points ie location to snap to and set of linestrings
# mh = f"""
#
# SELECT
#     f.gid as gid,
#     ST_Snap(f.Geometry, g.Geometry, 2) as geom
# FROM
#     pipe as f,
#     (SELECT ST_Collect(Geometry) as Geometry
#      FROM mh) as g
# """
#
# linest = f"""
#
# SELECT id, geom FROM {layer} a
#     WHERE NOT EXISTS
#      (SELECT 1 FROM {layer} b
#       WHERE a.id != b.id
#       AND   ST_Intersects(a.geom, b.geom))
# """