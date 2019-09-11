import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASSWORD')

con_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass}"

conn = psycopg2.connect(con_string)
cur = conn.cursor()
# cur.execute("select * from information_schema.tables where table_name=%s", ('mytable',))
# bool(cur.rowcount)

unique_floor_names = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'DG', 'EG', 'SO', 'U1', 'U2', 'U3', 'U4', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'ZD', 'ZE', 'ZU']


sql_campus = """CREATE TABLE geodata.buildings_campus
(
    id serial,
    campus_name character varying(128) COLLATE pg_catalog."default",
    description character varying(256) COLLATE pg_catalog."default",
    geom geometry(MultiPolygon,31259),
    fk_organization_id integer,
    PRIMARY KEY (id),
)
WITH (
    OIDS = FALSE
)"""

sql_building = """    CREATE TABLE geodata.buildings_building
(
    id serial,
    fk_campus_id integer,
    fk_organization_id integer
    PRIMARY KEY (id),

)
WITH (
    OIDS = FALSE
)"""


sql_floor = """
CREATE TABLE geodata.buildings_buildingfloor
(
    id serial,
    short_name character varying(150) COLLATE pg_catalog."default",
    long_name character varying(150) COLLATE pg_catalog."default",
    special_name character varying(150) COLLATE pg_catalog."default",
    vertical_order integer,
    base_elevation integer,
    floor_num integer,
    floor_height numeric(5,2),
    geom geometry(MultiPolygon,31259),
    fk_building_id integer,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)"""

def create_routing_tables(floor, campus="routing" ):

    sql_create = f"""CREATE TABLE routing.routing_networklines_{floor}
                    (
                        id serial,
                        name character varying(150) COLLATE pg_catalog."default",
                        speed numeric(10,2),
                        source integer,
                        target integer,
                        cost numeric(10,2),
                        length numeric(10,2),
                        floor_num integer,
                        network_type integer,
                        access_type character varying(150) COLLATE pg_catalog."default",
                        geom geometry(MultiLineString,31259),
                        fk_building_id integer,
                        PRIMARY KEY (id)
                    )
                    WITH (
                        OIDS = FALSE
                    ) """

    sql_del = f"""delete from routing.routing_networklines_{floor} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS routing.routing_networklines_{floor} CASCADE"
    sql_alter = f"""ALTER TABLE routing.routing_networklines_{floor} ADD COLUMN tags text[];"""
    sql_col = f"ALTER TABLE routing.routing_networklines_{floor} DROP COLUMN tag CASCADE;"


    # cur.execute(sql_drop)
    conn.commit()
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()




def create_umriss_table(floor, campus="campuses"):
    sql_create = f"""
            CREATE TABLE {campus}.indrz_umriss_{floor}
            (
                id serial,
                short_name character varying(150),
                long_name character varying(150),
                special_name character varying(150),
                vertical_order integer,
                base_elevation integer,
                floor_num integer,
                floor_height numeric(5,2),
                tags text[],
                geom geometry(MultiPolygon,31259),
                fk_building_id integer,
                PRIMARY KEY (id)
            )
            WITH (
                OIDS = FALSE
            )"""
    sql_del = f"""delete from {campus}.indrz_umriss_{floor} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS {campus}.indrz_umriss_{floor} CASCADE"
    sql_alter = f"""ALTER TABLE {campus}.indrz_umriss_{floor} ADD COLUMN tags text[];"""
    sql_col = f"ALTER TABLE {campus}.indrz_umriss_{floor} DROP COLUMN tag CASCADE;"


    cur.execute(sql_drop)
    conn.commit()
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()

def create_label_table(floor, campus="campuses"):
    campus = campus.lower()
    floor = str(floor)

    sql_create = f"""CREATE TABLE {campus}.indrz_labels_{floor}
    (
        id serial,
        short_name character varying(150) COLLATE pg_catalog."default",
        long_name character varying(150) COLLATE pg_catalog."default",
        floor_num integer,
        tags text[],
        geom geometry(MultiPoint,31259),
        fk_building_id integer,
        fk_building_floor_id integer,
        fk_line_type_id integer,
        PRIMARY KEY (id)
    )
    WITH (
        OIDS = FALSE
    )"""

    sql_lines_del = f"""delete from geodata.indrz_labels_{floor} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS {campus}.indrz_labels_{floor} CASCADE"

    # cur.execute(sql_drop)
    cur.execute(sql_create)
    conn.commit()


def create_spaces_table(floor, campus="campuses"):
    campus = campus.lower()
    floor = str(floor)
    sql_create = f"""CREATE TABLE {campus}.indrz_spaces_{floor}
    (
        id serial,
        short_name character varying(150) COLLATE pg_catalog."default",
        long_name character varying(150) COLLATE pg_catalog."default",
        area numeric(10,2),
        perimeter numeric(10,2),
        floor_num integer,
        geom geometry(MultiPolygon,31259),
        room_external_id character varying(150) COLLATE pg_catalog."default",
        room_number character varying(150) COLLATE pg_catalog."default",
        room_number_sign character varying(150) COLLATE pg_catalog."default",
        room_description character varying(150) COLLATE pg_catalog."default",
        room_code character varying(150) COLLATE pg_catalog."default",
        capacity integer,
        tag text,
        tags text[],
        fk_access_type_id integer,
        fk_building_id integer,
        fk_building_floor_id integer,
        space_type_id integer,
        PRIMARY KEY (id)
    )
    WITH (
        OIDS = FALSE
    )"""

    sql_del = f"""delete from geodata.indrz_spaces_{floor} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS {campus}.indrz_spaces_{floor} CASCADE"

    sql_alter = f"""ALTER TABLE campuses.indrz_spaces_{floor} ADD COLUMN tags text[];"""
    sql_col = f"ALTER TABLE {campus}.indrz_spaces_{floor} DROP COLUMN tag CASCADE;"



    # cur.execute(sql_drop)
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()




def create_lines_table(floor, campus="campuses", drop=False):
    campus = campus.lower()
    floor = str(floor)

    sql_create = f"""CREATE TABLE {campus}.indrz_lines_{floor}
    (
        id serial,
        short_name character varying(150) COLLATE pg_catalog."default",
        long_name character varying(150) COLLATE pg_catalog."default",
        length numeric(10,2),
        floor_num integer,
        tags text[],
        geom geometry(MultiLineString,31259),
        fk_building_id integer,
        fk_building_floor_id integer,
        fk_line_type_id integer,
        PRIMARY KEY (id)
    )
    WITH (
        OIDS = FALSE
    )"""

    sql_alter = f"""ALTER TABLE campuses.indrz_lines_{floor} ADD COLUMN tag text[];"""

    sql_alter2 = f"""ALTER TABLE campuses.indrz_lines_{floor} RENAME tag TO tags;"""

    sql_del = f"""delete from {campus}.indrz_lines_{floor} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS {campus}.indrz_lines_{floor} CASCADE"

    sql_col = f"ALTER TABLE {campus}.indrz_lines_{floor} DROP COLUMN tag CASCADE;"

    # cur.execute(sql_drop)
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()


def create_roomcode_points_table():

    # ['Name', 'Position X', 'Position Y', 'RAUMBEZEICHNUNG', 'RAUMNUMMER', 'Value', 'FLÄCHE', 'FLÄCHENART'],
    sql_create = """CREATE TABLE campuses.indrz_imported_roomcodes
    (
        id serial,
        campus character varying(150), -- the name of campus
        floor_num integer,
        cad_layer_name character varying(150),
        room_description character varying(150),
        room_external_id character varying(150),
        room_number character varying(150),
        room_number_sign character varying(150),
        room_code character varying(150),
        room_text character varying(150),
        tags text[],
        geom geometry(Point,31259),
        PRIMARY KEY (id)
    )
    WITH (
        OIDS = FALSE
    )"""

    sql_del = "delete from campuses.indrz_imported_roomcodes where 1 = 1;"
    sql_drop = "DROP TABLE IF EXISTS campuses.indrz_imported_roomcodes CASCADE"

    sql_alter = "ALTER TABLE campuses.indrz_imported_roomcodes ADD COLUMN tags text[];"
    sql_col = "ALTER TABLE campuses.indrz_imported_roomcodes DROP COLUMN tag CASCADE;"



    # cur.execute(sql_drop)
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()


# create_roomcode_points_table()




def create_empty_tables(campus="campuses", lines=False, spaces=False, labels=False, routing=False):
    for floor in unique_floor_names:
        if lines:
            create_lines_table(floor, campus)
        if spaces:
            create_spaces_table(floor, campus)
        if labels:
            create_label_table(floor, campus)
        if routing:
            create_routing_tables(floor)

# create_empty_tables(campus="routing", routing=True)
