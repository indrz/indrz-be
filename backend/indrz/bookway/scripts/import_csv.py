import csv
import psycopg2
import os


db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASS')

con_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass} port='5432'"
conn = psycopg2.connect(con_string)
cur = conn.cursor()


def import_data_20190822():
    with open(r"shelfdata_neu_ebene5_20190822.csv") as f:
        #shelf_ID;Seite;rvk Anfang;rvk Ende;floor
        creader = csv.DictReader(f, delimiter=';', dialect='excel', quotechar='|')
        next(creader, None)  # skip the headers
        for row in creader:
            # shelf_id;seite;rvk-start;rvk-ende;floor
            sql = f"""UPDATE django.bookway_shelfdata 
                       SET system_from = '{row['rvk-start']}', system_to = '{row['rvk-ende']}', side = '{row['seite']}'
                       WHERE django.bookway_shelfdata.external_id = '{row['shelf_id']}'
                       AND floor = {row['floor']}
                       AND side = '{row['seite']}'"""

            print(sql)
            conn.commit()


import_data_20190822()
conn.close()

def import_data_01_2019():
    with open(r"c:\Users\mdiener\Dropbox\00_GOMOGI\03_Projects\01_Current\12_1004_wu_wien_campusgis\shelfdata_neu_21-01-2019.CSV") as f:
        creader = csv.DictReader(f, delimiter=';', dialect='excel', quotechar='|')
        next(creader, None)  # skip the headers
        for row in creader:
            sql = f"INSERT INTO django.bookway_shelfdata (id, external_id, side, system_from, system_to, floor) " \
                f"values ({row['id']}," f"'{row['external_id']}', '{row['side']}', '{row['system_from']}', " \
                f"'{row['system_to']}', {row['floor']})"

            cur.execute(sql)

        sql_update_to = """update django.bookway_shelfdata set sys_to_array = regexp_split_to_array(system_to, '[ ]')
        where 1=1"""
        cur.execute(sql_update_to)

        sql_update_from = """update django.bookway_shelfdata set sys_from_array = regexp_split_to_array(system_from, '[ ]')
        where 1=1"""
        cur.execute(sql_update_from)

        sql_update_floor_id = """update django.bookway_shelfdata set building_floor_id = 68 where floor = 5"""
        cur.execute(sql_update_floor_id)

        sql_update_floor_id_6 = """update django.bookway_shelfdata set building_floor_id = 78 where floor = 6"""
        cur.execute(sql_update_floor_id_6)

        # note all shelfs are in LC and LC id = 2
        sql_update_building_id = """update django.bookway_shelfdata set building_id = 2 where 1 = 1"""
        cur.execute(sql_update_building_id)


        create_bookshelf_view = """CREATE or REPLACE view library.bookshelf as
            SELECT ogc_fid, id_letter, geom, 68 AS floor_id, 2 AS building_id from library.og05_library_regal_lines
            UNION
            SELECT ogc_fid, id_letter, geom, 78 AS floor_id, 2 AS building_id from library.og06_library_regal_lines;"""

        cur.execute(create_bookshelf_view)

        conn.commit()
        conn.close()
