import psycopg2
from utils import con_dj_string, unique_floor_names

# conn = psycopg2.connect(con_string_navigatur)
conn = psycopg2.connect(con_dj_string)
cur = conn.cursor()
# cur.execute("select * from information_schema.tables where table_name=%s", ('mytable',))
# bool(cur.rowcount)

unique_floor_map = [{'name': '1_0', 'number': 1.0, 'vis_name': 'OG01'},
                    {'name': '2_0', 'number': 2.0, 'vis_name': 'OG02'},
                    {'name': '3_0', 'number': 3.0, 'vis_name': 'OG03'},
                    {'name': '4_0', 'number': 4.0, 'vis_name': 'OG04'},
                    {'name': '5_0', 'number': 5.0, 'vis_name': 'OG05'},
                    {'name': '6_0', 'number': 6.0, 'vis_name': 'OG06'},
                    {'name': '0_0', 'number': 0.0, 'vis_name': 'EG'},
                    {'name': 'u1_0', 'number': -1.0, 'vis_name': 'UG01'}]

sql_forceClosed_linestrings = """
            CREATE OR REPLACE FUNCTION ST_ForceClosed(geom geometry)
              RETURNS geometry AS
            $BODY$BEGIN
              IF ST_IsClosed(geom) THEN
                RETURN geom;
              ELSIF GeometryType(geom) = 'LINESTRING' THEN
                SELECT ST_AddPoint(geom, ST_StartPoint(geom)) INTO geom;
              ELSIF GeometryType(geom) ~ '(MULTI|COLLECTION)' THEN
                -- Recursively deconstruct parts
                WITH parts AS (
                  SELECT ST_ForceClosed(gd.geom) AS closed_geom FROM ST_Dump(geom) AS gd
                ) -- Reconstitute parts
                SELECT ST_Collect(closed_geom) INTO geom
                FROM parts;
              END IF;
              IF NOT ST_IsClosed(geom) THEN
                RAISE EXCEPTION 'Could not close geometry';
              END IF;
              RETURN geom;
            END;$BODY$ LANGUAGE plpgsql IMMUTABLE COST 42;
            """


sql_campus = """CREATE TABLE geodata.buildings_campus
(
    id serial,
    campus_name character varying(128) COLLATE pg_catalog."default",
    description character varying(256) COLLATE pg_catalog."default",
    geom geometry(MultiPolygon,3857),
    fk_organization_id integer,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)"""

sql_building = """    CREATE TABLE geodata.buildings_building
(
    id serial primary key,
    fk_campus_id integer,
    fk_organization_id integer

)
WITH (
    OIDS = FALSE
)"""


def create_routing_tables(floor, schema="routing" ):

    sql_create = f"""CREATE TABLE {schema}.routing_networklines_{floor}
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




def create_umriss_table(floor, schema="pre_django"):
    sql_create = f"""
            CREATE TABLE {schema}.indrz_umriss_{floor}
            (
                id serial primary key,
                tags text[],
                geom geometry(MultiPolygon,3857),

            )
            WITH (
                OIDS = FALSE
            )"""
    sql_del = f"""delete from {schema}.indrz_umriss_{floor} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS {schema}.indrz_umriss_{floor} CASCADE"
    sql_alter = f"""ALTER TABLE {schema}.indrz_umriss_{floor} ADD COLUMN tags text[];"""
    sql_col = f"ALTER TABLE {schema}.indrz_umriss_{floor} DROP COLUMN tag CASCADE;"


    cur.execute(sql_drop)
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()

def create_label_table(floor, schema="pre_django"):

    sql_create = f"""CREATE TABLE {schema}.indrz_labels_{floor}
    (
        id serial primary key,
        tags text[],
        geom geometry(MultiPoint,3857)

    )
    WITH (
        OIDS = FALSE
    )"""

    sql_lines_del = f"""delete from {schema}.indrz_labels_{floor} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS {schema}.indrz_labels_{floor} CASCADE"

    # cur.execute(sql_drop)
    cur.execute(sql_create)
    conn.commit()


def create_outdoor(floor, schema="pre_django", drop_table=False):

    table_name_ply = f"{schema}.indrz_outdoor_poly_{floor}"
    table_name_line = f"{schema}.indrz_outdoor_line_{floor}"

    if drop_table:
        sql_del_ply = f"""delete from {table_name_ply} where 1 = 1;"""
        sql_drop_ply = F"DROP TABLE IF EXISTS {table_name_ply} CASCADE"
        sql_del = f"""delete from {table_name_line} where 1 = 1;"""
        sql_drop_line = F"DROP TABLE IF EXISTS {table_name_line} CASCADE"

        cur.execute(sql_drop_ply)
        cur.execute(sql_drop_line)


    sql_create_poly = f"""CREATE TABLE {table_name_ply}
    (
        id serial primary key ,
        geom geometry(MultiPolygon,3857),
        tags text[]
        
    )
    WITH (
        OIDS = FALSE
    )"""

    sql_create_line = f"""CREATE TABLE {table_name_line}
    (
        id serial primary key,
        tags text[],
        geom geometry(MultiLineString,3857)

    )
    WITH (
        OIDS = FALSE
    )"""


    cur.execute(sql_create_poly)
    cur.execute(sql_create_line)
    conn.commit()

def create_spaces_table(floor, schema="pre_django"):

    sql_create = f"""CREATE TABLE {schema}.indrz_spaces_{floor}
    (
        id serial primary key,
        tags text[],
        geom geometry(MultiPolygon,3857),
    )
    WITH (
        OIDS = FALSE
    )"""

    sql_del = f"""delete from geodata.indrz_spaces_{floor} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS {schema}.indrz_spaces_{floor} CASCADE"

    sql_alter = f"""ALTER TABLE campuses.indrz_spaces_{floor} ADD COLUMN tags text[];"""
    sql_col = f"ALTER TABLE {schema}.indrz_spaces_{floor} DROP COLUMN tag CASCADE;"



    # cur.execute(sql_drop)
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()




def create_lines_table(floor, campus="pre_django", drop=False):
    campus = campus.lower()
    floor = str(floor)

    sql_create = f"""CREATE TABLE {campus}.indrz_lines_{floor}
    (
        id serial primary key ,
        tags text[],
        geom geometry(MultiLineString,3857),
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


def create_interiorfloorsection_table(floor, campus="campuses"):
    t_name = f'{campus}.indrz_interiorfloorsection_{floor}'

    sql_create = f"""
            CREATE TABLE {t_name}
            (
                id serial,
                short_name character varying(150),
                floor_num integer,
                floor_name character varying(150),
                tags text[],
                geom geometry(MultiPolygon,31259),
                fk_building_floor_id integer,
                PRIMARY KEY (id)
            )
            WITH (
                OIDS = FALSE
            )"""
    sql_del = f"""delete from {t_name} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS {t_name} CASCADE"
    sql_alter = f"""ALTER TABLE {t_name} ADD COLUMN tags text[];"""
    sql_col = f"ALTER TABLE {t_name} DROP COLUMN tag CASCADE;"


    cur.execute(sql_drop)
    # conn.commit()
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()


def step1_create_empty_tables(schema="pre_django", lines=False, spaces=False, labels=False, routing=False, interiorfloorsection=False):

    cur.execute(sql_forceClosed_linestrings) # creates a function to enable generation of spaces from linestrings


    # create schema dxf_original;
    cur.execute("create schema if not exists pre_django;")
    cur.execute("create schema if not exists dxf_original;")

    conn.commit()

    for floor in unique_floor_names:
        if lines:
            create_lines_table(floor, schema)
        if spaces:
            create_spaces_table(floor, schema)
        if labels:
            create_label_table(floor, schema)
        if routing:
            create_routing_tables(floor)
        if interiorfloorsection:
            create_interiorfloorsection_table(floor)


def step2_create_roomcode_points_table():

    # ['Name', 'Position X', 'Position Y', 'RAUMBEZEICHNUNG', 'RAUMNUMMER', 'Value', "Layer", "RAUMCODE", "RAUMNR"],
    sql_create = """CREATE TABLE campuses.indrz_imported_roomcodes
    (
        id serial,
        campus character varying(150), -- the name of campus
        floor_num integer,
        floor_name character varying(150),
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

    cur.execute(sql_drop)
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()

if __name__ == '__main__':
    # step1_create_empty_tables(interiorfloorsection=True)
    create_label_table(floor='sou', )
    create_lines_table(floor='sou', )
    # create_spaces_table(floor='sou',)
    # create_outdoor(floor='eg', campus='campuses', drop_table=False)


    # update_space_id_by_color()

