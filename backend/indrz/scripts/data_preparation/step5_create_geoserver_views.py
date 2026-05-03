import psycopg2
import os
from utils import con_dj_string, floor_float_to_string, unique_floor_map

indrz_api_token = os.getenv('INDRZ_API_TOKEN')
GEOSERVER_USER = os.getenv('GEOSERVER_USER')
GEOSERVER_PASS = os.getenv('GEOSERVER_PASS')


# con_dj_string = f"dbname=indrzaau user=indrzaau host=campusplan-2023.aau.at password=qrKTadQij6tMHdATypa4Cu port=5432"

conn_dj = psycopg2.connect(con_dj_string)
cur_dj = conn_dj.cursor()


def drop_all_views():
    unique_floor_names = ['0.0', '1.0', '2.0', '3.0',]
    view_names = ['cartolines', 'spaces', 'anno', 'footprint']
    for view_name in view_names:
        for floor_name in unique_floor_names:
            q = f"""
            DROP VIEW IF EXISTS geodata.'{view_name}_{floor_name}';
            """
            # cur_dj.execute(q)
            # conn_dj.commit()


def create_cartolines_view():
    for floor in unique_floor_map:
        floor_float = floor['number']
        floor_name = floor_float_to_string(floor_float)
        q = f"""
        DROP VIEW IF EXISTS geodata.cartolines_{floor_name};
        CREATE OR REPLACE VIEW geodata.cartolines_{floor_name} AS
         SELECT buildings_buildingfloorplanline.id, buildings_buildingfloorplanline.short_name,
            buildings_buildingfloorplanline.geom
           FROM django.buildings_buildingfloorplanline
          WHERE django.buildings_buildingfloorplanline.floor_num = {floor_float};
        """
        print(q)
        cur_dj.execute(q)
        conn_dj.commit()


def create_spaces_view():
    for floor in unique_floor_map:
        floor_float = floor['number']
        floor_name = floor_float_to_string(floor_float)
        q_space = f"""
            DROP VIEW IF EXISTS geodata.spaces_{floor_name};
            CREATE OR REPLACE VIEW geodata.spaces_{floor_name} AS
            select fs.id,
                   fs.short_name,
                   fs.long_name as name,
                   fs.room_external_id,
                   fs.room_code,
                   fs.room_description,
                   b.building_name as building_name,
                   fs.space_type_id,
                   fs.capacity,
                   fs.floor_num,
                   fs.floor_name,                   
                   fs.geom
            FROM django.buildings_buildingfloorspace fs 
            LEFT JOIN django.buildings_building as b ON fs.fk_building_id = b.id
            WHERE fs.floor_num = {floor_float};
            ;

        """
        # q_space = f"""
        #     DROP VIEW IF EXISTS geodata.spaces_{floor_name};
        #     CREATE OR REPLACE VIEW geodata.spaces_{floor_name} AS
        #     select fs.id,
        #            r.zusatzbezeichnung as short_name,
        #            r.zusatzbezeichnung as name,
        #            fs.room_external_id,
        #            fs.room_code,
        #            fs.room_description,
        #            b.name as building_name,
        #            fs.space_type_id,
        #            fs.capacity,
        #            fs.floor_num,
        #            fs.floor_name,
        #            fs.geom
        #     FROM geodata.aaudata_2023 r
        #     JOIN django.buildings_buildingfloorspace fs on fs.room_code = r.raumnr
        #     JOIN django.buildings_building b ON b.id = fs.fk_building_id
        #     WHERE fs.floor_num = {floor_float};
        #
        #     ;
        #
        # """
        print(q_space)
        cur_dj.execute(q_space)
        conn_dj.commit()


def create_anno_view():
    for floor in unique_floor_map:
        floor_float = floor['number']
        floor_name = floor_float_to_string(floor_float)

        # only used if the AAU db would include all rooms
        # q_anno = f"""
        #         drop view if exists geodata.anno_{floor_name};
        #         CREATE OR REPLACE VIEW geodata.anno_{floor_name} AS
        #         select fs.id,
        #                fs.room_code,
        #                fs.room_description,
        #                fs.space_type_id,
        #                fs.long_name,
        #                r.raumbezeichnung as short_name,
        #                st_pointonsurface(fs.geom) as geom
        #         FROM geodata.aaudata_2023 r
        #         JOIN django.buildings_buildingfloorspace fs on fs.room_code = r.raumnr
        #               WHERE fs.floor_num = {floor_float}
        #                     AND fs.room_code is not null;
        #         """
        # AND d.id not in (SELECT d.id FROM django.buildings_buildingfloorspace AS d,
        #                                   django.buildings_interiorfloorsection AS ifc
        #                                  WHERE st_within(d.geom, ifc.geom)
        #                                         AND ifc.long_name = 'Baustelle');


        q_anno = f"""
            drop view if exists geodata.anno_{floor_name};
            CREATE OR REPLACE VIEW geodata.anno_{floor_name} AS
             SELECT d.id,
                 room_code,
                 room_description,
                 d.space_type_id,
                 d.long_name,
                 d.short_name,
                 st_pointonsurface(d.geom) as geom
              FROM django.buildings_buildingfloorspace as d
              WHERE d.floor_num = {floor_float} AND
              room_code is not null ;
        """
        cur_dj.execute(q_anno)
        conn_dj.commit()


def create_floor_footprint_view():
    for floor in unique_floor_map:
        floor_float = floor['number']
        floor_name = floor_float_to_string(floor_float)

        q_foot = f"""
        DROP VIEW IF EXISTS geodata.footprint_{floor_name};
        CREATE OR REPLACE VIEW geodata.footprint_{floor_name} AS
        SELECT bf.id, b.building_name, bf.geom, bf.floor_num
            FROM django.buildings_buildingfloor as bf
            join django.buildings_building as b on b.id = bf.fk_building_id
            WHERE floor_num = {floor_float};
        """
        print(q_foot)
        cur_dj.execute(q_foot)
        conn_dj.commit()


def create_routing_view():
    for floor in unique_floor_map:
        floor_float = floor['number']
        floor_name = floor_float_to_string(floor_float)

        q_route = f"""
            DROP VIEW IF EXISTS geodata.route_{floor_name};
            CREATE OR REPLACE VIEW geodata.route_{floor_name} AS
            SELECT id, floor_name, source, target, network_type, geom
            FROM geodata.networklines_3857
            WHERE floor = {floor_float};
        """
        print(q_route)
        cur_dj.execute(q_route)
        conn_dj.commit()


def create_construction_view():
    for floor in unique_floor_map:
        floor_float = floor['number']
        floor_name = floor_float_to_string(floor_float)

        q_route = f"""
            DROP VIEW IF EXISTS geodata.construction_{floor_name};
            CREATE OR REPLACE VIEW geodata.construction_{floor_name} AS
            SELECT id, short_name, organization, floor_name, floor_num, geom
            FROM django.buildings_interiorfloorsection
            WHERE floor_num = {floor_float};
        """
        print(q_route)
        cur_dj.execute(q_route)
        conn_dj.commit()


def create_wing_view():
    for floor in unique_floor_map:
        floor_float = floor['number']
        floor_name = floor_float_to_string(floor_float)

        q_route = f"""
            DROP VIEW IF EXISTS geodata.wing_{floor_name};
            CREATE OR REPLACE VIEW geodata.wing_{floor_name} AS
            SELECT id, name, abbreviation, '{floor_name}' as floor_name, '{floor_float}' as floor_num, geom
            FROM django.buildings_wing;
        """
        print(q_route)
        cur_dj.execute(q_route)
        conn_dj.commit()


def create_wing_points_view():
    for floor in unique_floor_map:
        floor_float = floor['number']
        floor_name = floor_float_to_string(floor_float)

        q_route = f"""
            DROP VIEW IF EXISTS geodata.wing_points_{floor_name};
            CREATE OR REPLACE VIEW geodata.wing_points_{floor_name} AS
            SELECT id, name, description, floor_name, floor_num, category_id, geom
            FROM django.poi_manager_poi
            WHERE floor_num = {floor_float}
            AND category_id in (80, 81) ;
        """
        print(q_route)
        cur_dj.execute(q_route)
        conn_dj.commit()


def create_entrances():
    q_entrance = f"""
        DROP VIEW IF EXISTS geodata.entrances;
        CREATE OR REPLACE VIEW geodata.entrances AS
        SELECT id, name, description, floor_name, floor_num, category_id, geom
        FROM django.poi_manager_poi
        WHERE floor_num = 0
        AND category_id in (31, 32);
    """
    cur_dj.execute(q_entrance)
    conn_dj.commit()


def create_campus_view():
    sql_campuses = f"""
        DROP VIEW IF EXISTS geodata.campuses;
        CREATE OR REPLACE VIEW geodata.campuses AS
        SELECT id, campus_name as name, description, geom
        FROM django.buildings_campus;
    """

    print(sql_campuses)
    cur_dj.execute(sql_campuses)
    conn_dj.commit()


def create_building_view():
    sql_campuses = f"""
        DROP VIEW IF EXISTS geodata.buildings;
        CREATE OR REPLACE VIEW geodata.buildings AS
        SELECT id, name, building_name, description, street, house_number, postal_code, city, geom
        FROM django.buildings_building;
    """

    print(sql_campuses)
    cur_dj.execute(sql_campuses)
    conn_dj.commit()


def create_search_v():
    sql_create_search_v = """
    -- create search_index_v
    DROP VIEW IF EXISTS geodata.search_index_v;
    CREATE OR REPLACE VIEW geodata.search_index_v(id, search_string, text_type, external_id, layer, building_id, campus_id, geom, room_code) as
        SELECT landscape_landscapearea.id,
           landscape_landscapearea.name             AS search_string,
           'landscapebuildings'::text               AS text_type,
           ''::text                                 AS external_id,
           0                                        AS layer,
           1                                        AS building_id,
           landscape_landscapearea.fk_campus_id     AS campus_id,
           st_force2d(landscape_landscapearea.geom) AS geom,
           ''::text                                 AS room_code
    FROM django.landscape_landscapearea
    WHERE landscape_landscapearea.name IS NOT NULL
    UNION
    SELECT buildings_buildingfloorspace.id,
           buildings_buildingfloorspace.room_code        AS search_string,
           'buildingfloorspace'::text                    AS text_type,
           buildings_buildingfloorspace.room_external_id AS external_id,
           buildings_buildingfloorspace.floor_num        AS layer,
           1   AS building_id,
           1                                             AS campus_id,
           st_force2d(buildings_buildingfloorspace.geom) AS geom,
           buildings_buildingfloorspace.room_code
    FROM django.buildings_buildingfloorspace
    WHERE buildings_buildingfloorspace.room_code IS NOT NULL
    UNION
    SELECT buildings_buildingfloorspace.id,
           buildings_buildingfloorspace.room_external_id AS search_string,
           'aks'::text                                   AS text_type,
           buildings_buildingfloorspace.room_external_id AS external_id,
           buildings_buildingfloorspace.floor_num        AS layer,
           1   AS building_id,
           1                                             AS campus_id,
           st_force2d(buildings_buildingfloorspace.geom) AS geom,
           buildings_buildingfloorspace.room_code
    FROM django.buildings_buildingfloorspace
    UNION
    SELECT poi_manager_poi.id,
           poi_manager_poi.name             AS search_string,
           'poi'::text                      AS text_type,
           ''::text                         AS external_id,
           poi_manager_poi.floor_num        AS layer,
           1   AS building_id,
           1                                AS campus_id,
           st_force2d(poi_manager_poi.geom) AS geom,
           ''::text                         AS room_code
    FROM django.poi_manager_poi
    WHERE poi_manager_poi.category_id <> 68
      AND poi_manager_poi.enabled IS TRUE
    UNION
    SELECT poi_manager_poi.id,
           poi_manager_poi.name_de          AS search_string,
           'poi'::text                      AS text_type,
           ''::text                         AS external_id,
           poi_manager_poi.floor_num        AS layer,
           1   AS building_id,
           1                                AS campus_id,
           st_force2d(poi_manager_poi.geom) AS geom,
           ''::text                         AS room_code
    FROM django.poi_manager_poi
    WHERE poi_manager_poi.category_id <> 68
      AND poi_manager_poi.enabled IS TRUE;"""

    print(sql_create_search_v)

    # cur_dj.execute(q_route)
    # conn_dj.commit()


def create_bookway_views():
    for floor in unique_floor_map:
        # floor_name = floor_float_to_string(floor_float)
        floor_name = floor['name']
        floor_float = floor['number']

        print(f"Creating BOOKWAY View: bookway_bookshelf_poly_{floor_name} and bookway_bookshelf_anno_{floor_name}")

        q_bookshelf_poly = f"""


                     DROP VIEW IF EXISTS geodata.bookway_bookshelf_poly_{floor_name};
                    CREATE VIEW geodata.bookway_bookshelf_poly_{floor_name} AS                     
                     select distinct on (bs.id) bs.id,
                                               bs.external_id,
                                               bf.floor_num,
                                               ST_Buffer(bs.geom, 0.25, 'endcap=flat join=round') as geom
                    from django.bookway_bookshelf bs
                    left join django.buildings_buildingfloor as bf on bf.id = bs.building_floor_id
                    where bf.floor_num = {floor_float};
                    """
        # print(q_bookshelf_poly)
        cur_dj.execute(q_bookshelf_poly)

        q_bookshelf_anno = f"""
             DROP VIEW IF EXISTS geodata.bookway_bookshelf_anno_{floor_name};
            create or replace view geodata.bookway_bookshelf_anno_{floor_name} as 
            select distinct on (bs.id) bs.id,
                           bs.external_id,
                           bs.left_from_label || '  ->  ' || bs.left_to_label as left_label,
                           bs.right_from_label || '  ->  ' ||  bs.right_to_label as right_label,
                           bs.double_faced,
                           building_floor_id,
                           bf.floor_name,
                           bf.floor_num,
                           bs.geom
                    from django.bookway_bookshelf bs
                    left join django.buildings_buildingfloor as bf on bf.id = bs.building_floor_id
                    where bf.floor_num = {floor_float};

        """

        cur_dj.execute(q_bookshelf_anno)

    conn_dj.commit()


if __name__ == "__main__":
    # NOTE TO SELF
    # NONE of these command delete data only insert
    # drop_all_views()
    # create_cartolines_view()
    # create_spaces_view()
    # create_campus_view()
    # create_building_view()
    # create_construction_view()
    # create_anno_view()
    # create_floor_footprint_view()
    # create_entrances()
    # create_wing_view()
    # create_wing_points_view()
    # create_search_v()
    # create_routing_view()
    create_bookway_views()
    conn_dj.close()

