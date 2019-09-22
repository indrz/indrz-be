import psycopg2


con_old_local_db = psycopg2.connect(host='localhost', user=db_old_user, port='5432', password=db_old_pwd, database=db_old_name)
cur_old_local_db = con_old_local_db.cursor()


con_new_local_db = psycopg2.connect(host='localhost', user=db_user, port='5432', password=db_pwd, database='indrzAau')
cur_new_local_db = con_new_local_db.cursor()

con_live_db = psycopg2.connect(host='campusplan.aau.at', user=db_prod_user, port='5432', password=db_prod_pwd, database=db_prod_name)
cur_live_db = con_new_local_db.cursor()

pg_schema = ('geodata')

table_abrev = ('e00_', 'e01_', 'e02_', 'e03_')

floor_values = ('poi', 'rooms', 'umriss', 'networklines', 'carto_lines', 'doors', 'furniture' )
other_tables = ('parking_garage', 'raumlist_buchungsys', 'temp_wu_personal_data' )
outdoor_tables = ('od_all_fill', 'od_all_polygons', 'od_baeume_linien', 'od_blindeleitlinie', 'od_fahrradstellplatz', 'od_familie_linie',
                  'od_orientierungselemente_linie', 'od_raucherzone', 'od_relax_area')
bibliothek_tables = ('bibliothek')



floors = [{"name": "e00_", "floor": 0}, {"name": "e01_", "floor": 1},
         {"name": "e02_", "floor": 2}, {"name": "e03_", "floor": 3}]

bib_floors = [{"name": "e01_", "floor": 1},
         {"name": "e02_", "floor": 2}, {"name": "e03_", "floor": 3}]



def create_shelf_anno():
    # select shelf
    sel_shelf = """SELECT bs.measure_from, bs.measure_to FROM django.library_bookshelf as bs
                    JOIN """



def create_bookway_shelf_views():

    for floor in bib_floors:
        floor_num = floor['floor']
        floor_name = floor['name']

        print(floor_num, floor_name)

        sql2 = """
                    DROP VIEW IF EXISTS geodata.{0}library_shelf_poly;
                    CREATE VIEW geodata.{0}library_shelf_poly AS SELECT DISTINCT ON (bs.id)
                     bs.id,
                     bs.external_id,
                     floor.floor_num,
                     shelfdata.sys_von,
                     shelfdata.sys_bis,
                     shelfdata.seite,
                     ST_Buffer(bs.geom, 0.25, 'endcap=flat join=round') as geom

                    FROM
                     django.library_bookshelf as bs

                    LEFT JOIN django.buildings_buildingfloor as floor ON bs.fk_building_floor_id = floor.id
                    LEFT JOIN bookway.shelfdata as shelfdata ON bs.external_id = shelfdata.external_id
                    WHERE bs.external_id LIKE 'Z{1}%' OR bs.external_id LIKE 'W{1}%'
                    ORDER BY bs.id, bs.external_id, shelfdata.seite, shelfdata.measure_from;""".format(floor_name, floor_num)
        print(sql2)
        cur_live_db.execute(sql2)
    res = con_live_db.commit()

create_bookway_shelf_views()

def create_view(floor, table):

    floor_level_txt = floor['name'] # "ug01"
    floor_name = floor['name']
    floor_num = str(floor['floor'])
    print(floor_level_txt)



    if table == 'carto_lines':
        q =  """
        -- DROP VIEW geodata.{0}{1};
        CREATE OR REPLACE VIEW geodata.{0}{1} AS
         SELECT buildings_buildingfloorplanline.id, buildings_buildingfloorplanline.short_name,
            buildings_buildingfloorplanline.geom
           FROM django.buildings_buildingfloorplanline
          WHERE buildings_buildingfloorplanline.floor_num = {2} ;

        """.format(floor_name, table, floor_num)

    if table == 'floor_footprint':
        q = """
            --drop view geodata.{0}{1};
            CREATE OR REPLACE VIEW geodata.{0}{1} AS
            SELECT f.name AS building_name, e.short_name AS floor_name, e.geom
            FROM django.buildings_buildingfloor AS e, django.buildings_building AS f
            WHERE e.fk_building_id = f.id AND e.floor_num = {2};
        """.format(floor_name, table, floor_num)

    # SELECT
    # d.room_code, w.bs_roomnr, w.fancyname_de, w.category_de, d.geom
    # from django.buildings_buildingfloorspace as d, wudata.raumlist_buchungsys as w
    # WHERE
    # d.room_external_id = w.pk_big;
    if table == 'space_polys':
        q = """
            --drop view geodata.{0}{1};
            CREATE OR REPLACE VIEW geodata.{0}{1} AS
            SELECT id,
                   short_name,
                   long_name,
                   room_code,
                   room_description,
                   space_type_id,
                   geom
                FROM django.buildings_buildingfloorspace
                WHERE floor_num = {2};
        """.format(floor_name, table, floor_num)

    if table == 'space_anno':
        q = """
            --drop view geodata.{0}{1};
            CREATE OR REPLACE VIEW geodata.{0}{1} AS
             SELECT d.id,
                 w.category_de as short_name,
                 w.roomname_de as long_name,
                 w.roomcode as room_code,
                 w.fancyname_de as room_description,
                 d.space_type_id,
                 d.geom
              FROM django.buildings_buildingfloorspace as d, wudata.raumlist_buchungsys as w
              WHERE d.room_external_id = w.pk_big AND d.floor_num = {2} ;
        """.format(floor_name, table, floor_num)
    # print('floor is now: ' + floor_num)
    # print(q)

    cur_new_local_db.execute(q)
    con_new_local_db.commit()


def run_create_view():
    # views = ('carto_lines', 'floor_footprint', 'space_polys')
    # views = ('carto_lines',)

    # create_view(floors, 'floor_footprint')


    for floor in floors:

        create_view(floor, 'space_polys')

        # for space in views:
        #
        #     create_view(floor, space)

# run_create_view()
