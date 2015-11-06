import os
import os.path
import psycopg2
# Database Connection Info
db_host = "localhost"
db_user = "indrz-pg"
db_passwd = "dm1vBJxpr70kkZO1udBY"
db_database = "indrz"
db_port = "5432"

conn = psycopg2.connect(host=db_host, user=db_user, port=db_port, password=db_passwd, database=db_database)
cur = conn.cursor()

floors = ["ug01", "e00", "e01", "e02", "e03"]
extension_name = "routing_networklines"
level = None

def cleanup():
    for floor in floors:
        cur.execute("""drop table if exists geodata.networklines_{0}""".format(floor))


def create_3D_networklines():
    for floor in floors:
        sql = """SELECT id, ST_Force_3d(ST_Transform(ST_Force_2D(st_geometryN(geom, 1)),3857)) AS geom,
          network_type, cost, length, 0 AS source, 0 AS target
          INTO geodata.networklines_{0}
          FROM geodata.routing_networklines{1}""".format(floor)

        cur.execute(sql)

create_3D_networklines()

def assign_z_elevation():
    for floor in floors:
        if floor == "ug01":
            level = -1
        elif floor == "e00":
            level = 0
        if floor == "e01":
            level = 1
        elif floor == "e02":
            level = 2
        elif floor == "e03":
            level = 3

        sql_update_3dz ="""UPDATE geodata.networklines_{0}
            SET geom=ST_Translate(ST_Force_3Dz(geom),0,0,{1}); """.format(floor, level)

        cur.execute(sql_update_3dz)
        cur.execute("""UPDATE geodata.networklines_{0} SET length =ST_Length(geom)""".format(floor))
        cur.execute("""UPDATE geodata.networklines_{0} SET cost=1 WHERE cost=0 or cost IS NULL; """.format(floor))
        cur.execute("""UPDATE geodata.networklines_{0} SET id=id+{1};""".format(floor,level+10000))


