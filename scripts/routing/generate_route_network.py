import os

import psycopg2
from dotenv import load_dotenv
load_dotenv()


db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASSWORD')

con_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass}"

conn = psycopg2.connect(con_string)
cur = conn.cursor()

schema = "geodata"

floors = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'DG', 'EG', 'SO',
                      'U1', 'U2', 'U3', 'U4', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'ZD', 'ZE', 'ZU']

def get_floor_float(name):
    """
    assuming input name is like "DA_EG_03_2019.dxf"
    :param name: dxf file name like "DA_EG_03_2019.dxf"
    :return: float value of floor
    """

    floor_names_odd = ['ZD', 'ZE', 'ZU', 'DG', 'EG', 'SO']
    floor_names_u = ['U1', 'U2', 'U3', 'U4']
    floor_names_z = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5']
    floor_names_int = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    if not name:
        return name
    floor = name.split("_")[-3]

    if floor in floor_names_odd:
        if floor == "EG":
            floor = 0.0
        elif floor == "SO":
            floor = -0.5
        elif floor == "ZE":
            floor = 0.5
        elif floor == "ZU":
            floor = -1.5
        else:
            floor = 9999.0
    elif floor in floor_names_z:
        # zwischen stock
        floor = float(floor[1])*1.0 + 0.5

    elif floor in floor_names_int:
        floor = float(floor)*1.0

    elif floor in floor_names_u:
        # underground
        floor = float(floor[1]) * -1.0
    else:
        floor = 9999.0


    return floor*1.0


def part1(schema, floors):

    for id, floor in enumerate(floors):

        temp_name = f"""xx_{floor}_xx_xx"""
        floor_float = get_floor_float(temp_name)

        temp_net_table = f"""{schema}.temp_networklines_{floor}"""
        src_networklines = f"""django.networklines_{floor}"""
        sql_setup = f"""
        -- if not, go ahead and update
        -- make sure tables dont exist
        
        drop table if exists {temp_net_table};
        
        -- convert to 3d coordinates with EPSG:3857
        
        SELECT id, ST_Force3D(ST_Transform(ST_Force2D(st_geometryN(geom, 1)),3857)) AS geom,
          network_type, cost::FLOAT, 0.0 AS reverse_cost, length, 0 AS source, 0 AS target
          INTO {temp_net_table}
          FROM {src_networklines};
        
        -- fill the 3rd coordinate according to their floor number
        
        UPDATE {temp_net_table} SET geom=ST_Translate(ST_Force3DZ(geom),0,0,{floor_float});
        
        UPDATE {temp_net_table} SET length =ST_Length(geom);
        
        -- no cost should be 0 or NULL/empty
        UPDATE {temp_net_table} SET cost=1 WHERE cost=0 or cost IS NULL;
        
        -- update unique ids id accordingly
        UPDATE {temp_net_table} SET id=id+{floor_float} + 100000.0;
        
        """
        print(sql_setup)
        # cur.execute(sql_setup)
        # conn.commit()


    merged_network_lines = "geodata.networklines_3857"

    t1 = """DROP TABLE IF EXISTS geodata.networklines_3857;"""
    print(t1)
    # cur.execute(t1)
    # conn.commit()

    for idx, floor in enumerate(floors):
        src_networklines = f"""django.networklines_{floor}"""

        temp_name = f"""xx_{floor}_xx_xx"""
        floor_float = get_floor_float(temp_name)

        insert_sql_network = f"""SELECT * INTO geodata.networklines_3857 FROM (SELECT id, geom length, network_type,
         length*e0.cost as cost, reverse_cost::DOUBLE PRECISION,
           {floor_float} as floor FROM {src_networklines} as e0);"""

        print(insert_sql_network)
        # cur.execute(insert_sql_network)
        # conn.commit()

    merge_it = f"""
        
        -- merge all networkline floors into a single table for routing
        
        UPDATE {merged_network_lines} set reverse_cost = cost;
        
        CREATE INDEX geom_gist_index
           ON {merged_network_lines} USING gist (geom);
        
        CREATE INDEX id_idx
           ON {merged_network_lines} USING btree (id ASC NULLS LAST);
        
        CREATE INDEX network_layer_idx
          ON {merged_network_lines}
          USING hash
          (floor);
        
        -- create populate geometry view with info
        SELECT Populate_Geometry_Columns('geodata.networklines_3857'::regclass);
        
        -- update stairs, ramps and elevators to match with the next layer
        UPDATE {merged_network_lines} SET geom=ST_AddPoint(geom,
          ST_EndPoint(ST_Translate(geom,0,0,1)))
          WHERE network_type=1 OR network_type=2 OR network_type=5;
        -- remove the second last point
        UPDATE {merged_network_lines} SET geom=ST_RemovePoint(geom,ST_NPoints(geom) - 2)
          WHERE network_type=1 OR network_type=2 OR network_type=5;
        
        
        -- add columns source and target
        ALTER TABLE {merged_network_lines} add column source integer;
        ALTER TABLE {merged_network_lines} add column target integer;"""

    print(merge_it)
    # cur.execute(merge_it)
    # conn.commit()


    for id, floor in enumerate(floors):
        temp_net_table = f"""DROP TABLE IF EXISTS {schema}.temp_networklines_{floor}"""

        print(temp_net_table)
        # cur.execute(temp_net_table)
        # conn.commit()

    last_work_sql = f"""
        -- remove route nodes vertices table if exists
        DROP TABLE IF EXISTS geodata.networklines_3857_vertices_pgr;
        -- building routing network vertices (fills source and target columns in those new tables)
        SELECT public.pgr_createtopology3dIndrz('{merged_network_lines}', 0.0001, 'geom', 'id', 'source', 'target', 'true', true);
    
        DELETE FROM {merged_network_lines} WHERE cost ISNULL;
        --ALTER TABLE geodata.networklines_3857_vertices_pgr OWNER TO "indrz-wu";
    
        """

    print(last_work_sql)
    # cur.execute(last_work_sql)
    # conn.commit()


part1("geodata",floors)
