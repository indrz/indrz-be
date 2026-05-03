import os
import psycopg2
import time
from utils import get_floor_float

db_user = os.getenv('POSTGRES_USER')
db_name = os.getenv('POSTGRES_DB')
db_host = os.getenv('POSTGRES_HOST')
db_pass = os.getenv('POSTGRES_PASS')
db_port = os.getenv('POSTGRES_PORT')
indrz_api_token = os.getenv('INDRZ_API_TOKEN')
GEOSERVER_USER = os.getenv('GEOSERVER_USER')
GEOSERVER_PASS = os.getenv('GEOSERVER_PASS')




unique_floor_map = [{'name': '0_0', 'number': 0.0, 'vis_name': 'EG'},
                    {'name': '1_0', 'number': 1.0, 'vis_name': 'OG01'},
                    {'name': '2_0', 'number': 2.0, 'vis_name': 'OG02'},
                    {'name': '3_0', 'number': 3.0, 'vis_name': 'OG03'},
                    {'name': '4_0', 'number': 4.0, 'vis_name': 'OG04'},
                    {'name': '5_0', 'number': 5.0, 'vis_name': 'OG05'}
                    ]


conn = psycopg2.connect(host=db_host, user=db_user, port=db_port,
                         password=db_pass, database=db_name)
cur = conn.cursor()


con_string = f"dbname={db_name} user={db_user} host={db_host} port={db_port} password={db_pass}"
schema = "geodata"


def hotfix():
    for floor_data in unique_floor_map:

        floor = floor_data['name']
        vis_name = floor_data['vis_name']
        # floor_float = floor['number']
        seq_name = f"geodata.routing_networklines_{floor}_id_seq"


        # s = f"""ALTER TABLE routing.routing_networklines_{floor.lower()} ADD COLUMN floor_name character varying;"""
        # cur.execute(s)
        #
        # up = f"""UPDATE routing.routing_networklines_{floor.lower()} SET floor_name='{str(floor_float)}';
        #          UPDATE routing.routing_networklines_{floor.lower()} SET floor_num={floor_float};
        #       """

        mor_fix = f"""
        

        
        CREATE TABLE geodata.routing_networklines_{floor} AS TABLE django.routing_networklines_{floor};
        ALTER TABLE geodata.routing_networklines_{floor} ADD floor_name VARCHAR;
        UPDATE geodata.routing_networklines_{floor} SET floor_name ='{vis_name}' where floor_name is null;
        ALTER TABLE geodata.routing_networklines_{floor} ALTER COLUMN id SET NOT NULL;

        ALTER TABLE geodata.routing_networklines_{floor} ADD PRIMARY KEY (id);
        
        -- Step 1: Create a sequence
        CREATE SEQUENCE geodata.routing_networklines_{floor}_id_seq;
        -- Step 2: Set the next value of the sequence as the default value for id
        ALTER TABLE geodata.routing_networklines_{floor} ALTER COLUMN id SET DEFAULT nextval('{seq_name}');
        -- Optionally, to ensure the sequence starts at the right number, find the maximum id and set the sequence to start from there
        SELECT setval('{seq_name}', MAX(id)) FROM geodata.routing_networklines_{floor};
        



        """
        print("doing ", floor)
        cur.execute(mor_fix)
        conn.commit()


def generate_3d_routing_network(schema):
    merged_network_lines = f"geodata.networklines_3857"

    for floor_data in unique_floor_map:
        floor = floor_data['name']
        floor_float = floor_data['number']

        # temp_name = f"""xx_{floor}_xx_xx"""


        temp_net_table = f"""{schema}.temp_networklines_{floor}"""
        src_networklines = f"""{schema}.routing_networklines_{floor}"""
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
        UPDATE {temp_net_table} SET floor_name='{floor_data['vis_name']}';

        """
        print("GENERATING TEMP temp_networklines,", floor)
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
                    OWNER to indrzaau;
    """
    cur.execute(t1)
    conn.commit()

    print(f"inserting data into floors  table: {merged_network_lines}")

    for floor_data in unique_floor_map:
        floor = floor_data['name']
        floor_float = floor_data['number']

        floor = floor.lower()
        src_networklines = f"""{schema}.temp_networklines_{floor}"""

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
          WHERE network_type=1 OR network_type=2 OR network_type=3 OR network_type=5;
        -- remove the second last point
        UPDATE {merged_network_lines} SET geom=ST_RemovePoint(geom,ST_NPoints(geom) - 2)
          WHERE network_type=1 OR network_type=2 OR network_type=3 OR network_type=5;


        -- add columns source and target
        ALTER TABLE {merged_network_lines} add column source integer;
        ALTER TABLE {merged_network_lines} add column target integer;"""

    print("UDPATING merged networklines attributes source features")
    cur.execute(merge_it)
    conn.commit()


    print("REMOVING TEMP tables")
    for floor_data in unique_floor_map:
        floor = floor_data['name']
        floor = floor.lower()
        temp_net_table = f"""DROP TABLE IF EXISTS {schema}.temp_networklines_{floor}"""

        cur.execute(temp_net_table)
        conn.commit()

    last_work_sql = f"""
        -- remove route nodes vertices table if exists
        DROP TABLE IF EXISTS {merged_network_lines}_vertices_pgr;
        -- building routing network vertices (fills source and target columns in those new tables)
        SELECT public.pgr_createtopology3dIndrz('{merged_network_lines}', 0, 'geom', 'id', 'source', 'target', 'true', true);

        DELETE FROM {merged_network_lines} WHERE cost ISNULL;
        DELETE FROM {merged_network_lines} WHERE length = 0;
        ALTER TABLE {merged_network_lines}_vertices_pgr OWNER TO "indrzaau";

        """

    print("creating topo 3d")
    cur.execute(last_work_sql)
    conn.commit()


if __name__ == '__main__':
    # hotfix()
    start_time = time.time()
    print(f"time to start is {start_time}")
    generate_3d_routing_network("geodata")
    conn.close()

    end_time = time.time()
    print(f"time to end is {end_time}")
    # Calculate the elapsed time in seconds
    elapsed_time = end_time - start_time

    # Convert the elapsed time to minutes and seconds
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    print(f"Script ran for {minutes} minutes and {seconds} seconds.")
