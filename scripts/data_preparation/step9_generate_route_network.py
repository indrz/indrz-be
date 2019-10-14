import os

import psycopg2
from dotenv import load_dotenv

from utils import get_floor_float

load_dotenv()

db_user = os.getenv('POSTGRES_USER_LIVE')
db_name = os.getenv('POSTGRES_DB_LIVE')
db_host = os.getenv('POSTGRES_HOST_LIVE')
db_pass = os.getenv('POSTGRES_PASS_LIVE')
db_port = os.getenv('POSTGRES_PORT_LIVE')

con_string = f"dbname={db_name} user={db_user} host={db_host} port={db_port} password={db_pass}"

conn = psycopg2.connect(con_string)
cur = conn.cursor()

schema = "geodata"

floors = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'DG', 'EG', 'SO','U1', 'U2', 'U3',
          'U4', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'ZD', 'ZE', 'ZU']

def hotfix(floors):
    for floor in floors:
        s = f"""ALTER TABLE routing.routing_networklines_{floor.lower()} ADD COLUMN floor_name character varying;"""
        cur.execute(s)
        conn.commit()
        up = f"""UPDATE routing.routing_networklines_{floor.lower()} SET floor_name='{floor.lower()}';"""
        cur.execute(up)
        conn.commit()


def part1(schema, floors):
    merged_network_lines = "geodata.networklines_3857"

    for floor in floors:
        floor_float = get_floor_float(floor)
        floor = floor.lower()

        # temp_name = f"""xx_{floor}_xx_xx"""


        temp_net_table = f"""{schema}.temp_networklines_{floor}"""
        src_networklines = f"""routing.routing_networklines_{floor}"""
        sql_setup = f"""
        -- if not, go ahead and updateindrztu
        -- make sure tables dont exist
        
        drop table if exists {temp_net_table};
        
        -- convert to 3d coordinates with EPSG:3857
        
        SELECT id, ST_Force3D(ST_Transform(ST_Force2D(st_geometryN(geom, 1)),3857)) AS geom,
          network_type, cost::FLOAT, 0.0 AS reverse_cost, length, 0 AS source, 0 AS target, floor_name
          INTO {temp_net_table}
          FROM {src_networklines};
        
        -- fill the 3rd coordinate according to their floor number
        
        UPDATE {temp_net_table} SET geom=ST_Translate(ST_Force3DZ(geom),0,0,{floor_float});
        
        UPDATE {temp_net_table} SET length =ST_Length(geom);
        
        -- no cost should be 0 or NULL/empty
        UPDATE {temp_net_table} SET cost=1 WHERE cost=0 or cost IS NULL;
        
        -- update unique ids id accordingly
        UPDATE {temp_net_table} SET id=id+{floor_float} + 100000.0;
        
        -- update floor-name
        UPDATE {temp_net_table} SET floor_name='{floor}';
        
        """
        print("GENERATING TEMP temp_networklines")
        # print(sql_setup)
        cur.execute(sql_setup)
        conn.commit()

    t1 = f"""DROP TABLE IF EXISTS {merged_network_lines};
            CREATE TABLE {merged_network_lines}
                (
                    id serial PRIMARY KEY,
                    geom geometry,
                    length numeric(10,2),
                    network_type integer,
                    cost double precision,
                    reverse_cost double precision,
                    floor double precision,
                    floor_name character varying
                )
                WITH (
                    OIDS = FALSE
                )
                TABLESPACE pg_default;
                
                ALTER TABLE {merged_network_lines}
                    OWNER to tu;
    """
    print(t1)
    cur.execute(t1)
    conn.commit()

    for floor in floors:

        floor_float = get_floor_float(floor)
        print(f"FLOOOOOR IS     {floor} the {floor_float}")
        floor = floor.lower()
        src_networklines = f"""{schema}.temp_networklines_{floor}"""

        print(f"FLOOR FLOAT IS {floor_float}")

        insert_sql_network = f"""INSERT INTO {merged_network_lines} (geom, length, network_type, 
                                                cost, reverse_cost, floor, floor_name)
                            SELECT geom, length, network_type, length*e0.cost as cost, 
                            reverse_cost::DOUBLE PRECISION, {floor_float} as floor, floor_name FROM {src_networklines} as e0;"""

        print(f"inserting data into {merged_network_lines}")
        cur.execute(insert_sql_network)
        conn.commit()

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
        SELECT Populate_Geometry_Columns('{merged_network_lines}'::regclass);
        
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

    print("UDPATING merged networklines attributes source features")
    cur.execute(merge_it)
    conn.commit()


    print("REMOVING TEMP tables")
    for id, floor in enumerate(floors):
        floor = floor.lower()
        temp_net_table = f"""DROP TABLE IF EXISTS {schema}.temp_networklines_{floor}"""


        cur.execute(temp_net_table)
        conn.commit()

    last_work_sql = f"""
        -- remove route nodes vertices table if exists
        DROP TABLE IF EXISTS {merged_network_lines}_vertices_pgr;
        -- building routing network vertices (fills source and target columns in those new tables)
        SELECT public.pgr_createtopology3dIndrz('{merged_network_lines}', 0.0001, 'geom', 'id', 'source', 'target', 'true', true);
    
        DELETE FROM {merged_network_lines} WHERE cost ISNULL;
        ALTER TABLE {merged_network_lines}_vertices_pgr OWNER TO "tu";
    
        """

    print("creating topo 3d")
    cur.execute(last_work_sql)
    conn.commit()


if __name__ == '__main__':
    # hotfix(floors)
    part1("geodata", floors)
    conn.close()
