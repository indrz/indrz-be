import psycopg2
from utils import unique_floor_names, get_floor_float
from utils import con_string, con_dj_string, unique_floor_names


conn_dj = psycopg2.connect(con_dj_string)
cur_dj = conn_dj.cursor()

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
            SELECT long_name AS building_name, geom
            FROM django.buildings_buildingfloor
            WHERE floor_num = {floor_float};
        """
        cur_dj.execute(q_footprint)
        conn_dj.commit()


if __name__ == "__main__":
    # NOTE TO SELF
    # NONE of these command delete data only insert
    # create_cartolines_view()
    # create_spaces_view()
    create_floor_footprint_view()

