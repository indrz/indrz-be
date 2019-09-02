import os
import psycopg2

con_string = "dbname=" + os.getenv('DB_NAME') + " user=" + os.getenv('DB_USER') + " host=" + os.getenv('DB_HOST') + " password=" + os.getenv('DB_PASSWORD')

conn = psycopg2.connect(con_string)
cur = conn.cursor()


sql = """ SELECT ST_AsText(ST_Split(ST_Snap(n.geom, p.geom, 1), p.geom)) 
    FROM starting_network n, cut_points_multi p;"""

split_lines_query = """ CREATE TABLE geodata.split_roads
    AS SELECT(ST_Dump(ST_Node
        (ST_Collect(wkb_geometry)))).geom AS geom
    FROM geodata.lines;
                     """
cur.execute(split_lines_query)
conn.commit()

# close cursor
cur.close()

# close connection
conn.close()