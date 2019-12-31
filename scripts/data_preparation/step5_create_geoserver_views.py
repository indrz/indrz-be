import psycopg2
from utils import unique_floor_names, get_floor_float
from utils import con_string_navigatur, unique_floor_names, con_tuindrz

conn_dj = psycopg2.connect(con_string_navigatur) # tuw-maps.tuwien.ac.at
# conn_dj = psycopg2.connect(con_tuindrz) # tu.indrz.com
cur_dj = conn_dj.cursor()

def drop_all_views():
    view_names = ['cartolines', 'spaces', 'anno', 'footprint']
    for view_name in view_names:
        for floor_name in unique_floor_names:

            q = f"""
            DROP VIEW IF EXISTS geodata.{view_name}_{floor_name};
            """
            cur_dj.execute(q)
            conn_dj.commit()


def create_cartolines_view():

    for floor_name in unique_floor_names:


        q =  f"""
        DROP VIEW IF EXISTS geodata.cartolines_{floor_name};
        CREATE OR REPLACE VIEW geodata.cartolines_{floor_name} AS
         SELECT buildings_buildingfloorplanline.id, buildings_buildingfloorplanline.short_name,
            buildings_buildingfloorplanline.geom
           FROM django.buildings_buildingfloorplanline
          WHERE buildings_buildingfloorplanline.floor_name = '{floor_name}' ;
        """

        cur_dj.execute(q)
        conn_dj.commit()

def create_spaces_view():

    for floor_name in unique_floor_names:
        floor_float = get_floor_float(floor_name)

        q_space = f"""
            DROP VIEW IF EXISTS geodata.spaces_{floor_name};
            CREATE OR REPLACE VIEW geodata.spaces_{floor_name} AS
            SELECT id,
                   short_name,
                   room_code,
                   room_description,
                   space_type_id,
                   floor_num,
                   floor_name,
                   geom
                FROM django.buildings_buildingfloorspace
                WHERE floor_num = {floor_float};
        """
        cur_dj.execute(q_space)
        conn_dj.commit()

        q_anno = f"""
            drop view if exists geodata.anno_{floor_name};
            CREATE OR REPLACE VIEW geodata.anno_{floor_name} AS
             SELECT d.id,
                 room_code,
                 room_description,
                 d.space_type_id,
                 d.geom
              FROM django.buildings_buildingfloorspace as d
              WHERE d.floor_num = {floor_float} AND
              room_code is not null ;
        """
        cur_dj.execute(q_anno)
        conn_dj.commit()


def create_floor_footprint_view():
    for floor_name in unique_floor_names:
        floor_float = get_floor_float(floor_name)

        q_footprint = f"""
            DROP VIEW IF EXISTS geodata.footprint_{floor_name};
            CREATE OR REPLACE VIEW geodata.footprint_{floor_name} AS
            SELECT id, long_name AS building_name, geom
            FROM django.buildings_buildingfloor
            WHERE floor_num = {floor_float};
        """
        cur_dj.execute(q_footprint)
        conn_dj.commit()

def create_routing_view():
    for floor_name in unique_floor_names:
        floor_float = get_floor_float(floor_name)

        q_route = f"""
            DROP VIEW IF EXISTS geodata.route_{floor_name};
            CREATE OR REPLACE VIEW geodata.route_{floor_name} AS
            SELECT id, floor_name, source, target, network_type, geom
            FROM geodata.networklines_3857
            WHERE floor = {floor_float};
        """
        cur_dj.execute(q_route)
        conn_dj.commit()

def create_construction_view():
    for floor_name in unique_floor_names:
        floor_float = get_floor_float(floor_name)

        q_route = f"""
            DROP VIEW IF EXISTS geodata.construction_{floor_name};
            CREATE OR REPLACE VIEW geodata.construction_{floor_name} AS
            SELECT id, short_name, organization, floor_name, floor_num, geom
            FROM django.buildings_interiorfloorsection
            WHERE floor_num = {floor_float};
        """
        cur_dj.execute(q_route)
        conn_dj.commit()


def create_wing_view():
    for floor_name in unique_floor_names:
        floor_float = get_floor_float(floor_name)

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
    for f_name in unique_floor_names:
        floor_float = get_floor_float(f_name)

        q_route = f"""
            DROP VIEW IF EXISTS geodata.wing_points_{f_name};
            CREATE OR REPLACE VIEW geodata.wing_points_{f_name} AS
            SELECT id, name, floor_name, floor_num, geom
            FROM django.poi_manager_poi
            WHERE floor_name = '{f_name}'
            AND category_id = 80 ;
        """
        print(q_route)
        cur_dj.execute(q_route)
        conn_dj.commit()

if __name__ == "__main__":
    # NOTE TO SELF
    # NONE of these command delete data only insert
    # drop_all_views()
    # create_cartolines_view()
    # create_spaces_view()
    # create_floor_footprint_view()
    # create_routing_view()
    # create_construction_view()
    # create_wing_view()
    create_wing_points_view()
    conn_dj.close()

