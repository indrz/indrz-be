import psycopg2
import os

db_user = os.getenv('PG_USER')
db_name = os.getenv('PG_DB')
db_host = os.getenv('PG_HOST')
db_pass = os.getenv('PG_PASS')
db_port = os.getenv('PG_PORT')
GEOSERVER_USER = os.getenv('GEOSERVER_USER')
GEOSERVER_PASS = os.getenv('GEOSERVER_PASS')

dxf_root_path = os.getenv('DXF_ROOT_PATH')

con_dj_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass} port={db_port}"


# conn = psycopg2.connect(con_string_navigatur)
conn = psycopg2.connect(con_dj_string)
cur = conn.cursor()
# cur.execute("select * from information_schema.tables where table_name=%s", ('mytable',))
# bool(cur.rowcount)




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


sql_campus = f"""CREATE TABLE {schema}.buildings_campus
(
    id serial,
    campus_name character varying(128) COLLATE pg_catalog."default",
    description character varying(256) COLLATE pg_catalog."default",
    geom geometry(MultiPolygon,31259),
    fk_organization_id integer,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)"""

sql_building = f"""CREATE TABLE {schema}.buildings_building
(
    id serial,
    fk_campus_id integer,
    fk_organization_id integer
    PRIMARY KEY (id)

)
WITH (
    OIDS = FALSE
)"""


sql_floor = f"""
CREATE TABLE {schema}.buildings_buildingfloor
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

def create_routing_tables(floor, schema="geodata" ):

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

    sql_del = f"""delete from {schema}.routing_networklines_{floor} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS {schema}.routing_networklines_{floor} CASCADE"
    sql_alter = f"""ALTER TABLE {schema}.routing_networklines_{floor} ADD COLUMN tags text[];"""
    sql_col = f"ALTER TABLE {schema}.routing_networklines_{floor} DROP COLUMN tag CASCADE;"


    # cur.execute(sql_drop)
    conn.commit()
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()




def create_umriss_table(floor, schema="pre_django"):
    sql_create = f"""
            CREATE TABLE {schema}.indrz_umriss_{floor}
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
    sql_del = f"""delete from {schema}.indrz_umriss_{floor} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS {schema}.indrz_umriss_{floor} CASCADE"
    sql_alter = f"""ALTER TABLE {schema}.indrz_umriss_{floor} ADD COLUMN tags text[];"""
    sql_col = f"ALTER TABLE {schema}.indrz_umriss_{floor} DROP COLUMN tag CASCADE;"


    cur.execute(sql_drop)
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()

def create_label_table(floor, schema="pre_django"):
    schema = schema.lower()
    floor = str(floor)

    sql_create = f"""CREATE TABLE {schema}.indrz_labels_{floor}
    (
        id serial,
        short_name character varying(150) COLLATE pg_catalog."default",
        long_name character varying(150) COLLATE pg_catalog."default",
        floor_num float,
        floor_name character varying,
        room_code character varying,
        room_external_id character varying,
        tags text[],
        geom geometry(MultiPoint,31259),
        fk_building_id integer,
        fk_building_floor_id integer,
        fk_line_type_id integer,
        space_type_id integer,
        PRIMARY KEY (id)
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
    schema = schema.lower()
    floor = str(floor)
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
        id serial,
        name character varying(150),
        type character varying(150),
        floor_num integer,
        geom geometry(MultiPolygon,31259),
        tags text[],
        PRIMARY KEY (id)
    )
    WITH (
        OIDS = FALSE
    )"""

    sql_create_line = f"""CREATE TABLE {table_name_line}
    (
        id serial,
        name character varying(150),
        type character varying(150),
        floor_num integer,
        geom geometry(MultiLineString,31259),
        tags text[],
        PRIMARY KEY (id)
    )
    WITH (
        OIDS = FALSE
    )"""


    cur.execute(sql_create_poly)
    cur.execute(sql_create_line)
    conn.commit()

def create_spaces_table(floor, schema="pre_django"):
    schema = schema.lower()
    floor = str(floor)
    sql_create = f"""CREATE TABLE {schema}.indrz_spaces_{floor}
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

    sql_del = f"""delete from {schema}.indrz_spaces_{floor} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS {schema}.indrz_spaces_{floor} CASCADE"

    sql_alter = f"""ALTER TABLE {schema}.indrz_spaces_{floor} ADD COLUMN tags text[];"""
    sql_col = f"ALTER TABLE {schema}.indrz_spaces_{floor} DROP COLUMN tag CASCADE;"



    # cur.execute(sql_drop)
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()




def create_lines_table(floor, schema="pre_django", drop=False):
    schema = schema.lower()
    floor = str(floor)

    sql_create = f"""CREATE TABLE {schema}.indrz_lines_{floor}
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

    sql_alter = f"""ALTER TABLE {schema}.indrz_lines_{floor} ADD COLUMN tag text[];"""

    sql_alter2 = f"""ALTER TABLE {schema}.indrz_lines_{floor} RENAME tag TO tags;"""

    sql_del = f"""delete from {schema}.indrz_lines_{floor} where 1 = 1;"""
    sql_drop = F"DROP TABLE IF EXISTS {schema}.indrz_lines_{floor} CASCADE"

    sql_col = f"ALTER TABLE {schema}.indrz_lines_{floor} DROP COLUMN tag CASCADE;"

    # cur.execute(sql_drop)
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()

def create_tu_data_table(schema="geodata"):

    # ['Name', 'Position X', 'Position Y', 'RAUMBEZEICHNUNG', 'RAUMNUMMER', 'Value', "Layer", "RAUMCODE", "RAUMNR"],
    sql_create = f"""CREATE TABLE {schema}.tu_data
    (
        id serial primary key ,
        room_code character varying(150),
        wing character varying(150),
        floor character varying(150),
        room_number character varying(150),
        main_use character varying(150),
        color character varying(150),
        description character varying(150)
    )
    WITH (
        OIDS = FALSE
    )"""

    sql_drop = f"DROP TABLE IF EXISTS {schema}.tu_data CASCADE"

    alt = f"alter table {schema}.tu_data owner to tu;"

    cur.execute(sql_drop)
    cur.execute(sql_create)
    cur.execute(alt)
    conn.commit()


def create_interiorfloorsection_table(floor, schema="pre_django"):
    t_name = f'{schema}.indrz_interiorfloorsection_{floor}'

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


def init_pre_django_tables(schema="pre_django", lines=False, spaces=False, labels=False, routing=False, interiorfloorsection=False):

    cur.execute(sql_forceClosed_linestrings) # creates a function to enable generation of spaces from linestrings
    conn.commit()

    for floor_info in unique_floor_map:
        floor = floor_info.get('num_txt_code')
        if lines:
            create_lines_table(floor, schema)
        if spaces:
            create_spaces_table(floor, schema)
        if labels:
            create_label_table(floor, schema)
        if routing:
            create_routing_tables(floor, schema="geodata")
        if interiorfloorsection:
            create_interiorfloorsection_table(floor, schema)



def step2_create_roomcode_points_table(schema="pre_django"):

    # ['Name', 'Position X', 'Position Y', 'RAUMBEZEICHNUNG', 'RAUMNUMMER', 'Value', "Layer", "RAUMCODE", "RAUMNR"],
    sql_create = f"""CREATE TABLE {schema}.indrz_imported_roomcodes
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

    sql_del = f"delete from {schema}.indrz_imported_roomcodes where 1 = 1;"
    sql_drop = f"DROP TABLE IF EXISTS {schema}.indrz_imported_roomcodes CASCADE"
    sql_alter = f"ALTER TABLE {schema}.indrz_imported_roomcodes ADD COLUMN tags text[];"
    sql_col = f"ALTER TABLE {schema}.indrz_imported_roomcodes DROP COLUMN tag CASCADE;"



    cur.execute(sql_drop)
    cur.execute(sql_create)
    # cur.execute(sql_col)
    conn.commit()

if __name__ == '__main__':

    ## requires a list of unique floors across all buildings
    unique_floor_map = [{'num_txt_code': '0_0', 'number': 0.0, 'name': 'EG'},
                    {'num_txt_code': '1_0', 'number': 1.0, 'name': 'OG01'},
                    {'num_txt_code': '2_0', 'number': 2.0, 'name': 'OG02'},
                    {'num_txt_code': '3_0', 'number': 3.0, 'name': 'OG03'}
                    ]
    
    if unique_floor_map:

        init_pre_django_tables(interiorfloorsection=True)
        # create_label_table(floor='sou', )
        # create_lines_table(floor='sou', )
        # create_spaces_table(floor='sou',)
        # create_outdoor(floor='eg', schema='pre_django', drop_table=False)
        # create_tu_data_table()
        # update_space_id_by_color()

    else:
        print("No unique floors defined! Please define unique floors across all buildings before creating tables.")



