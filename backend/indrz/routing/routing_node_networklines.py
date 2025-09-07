import time
import logging
import os
import psycopg2
from .utils import get_floor_float, unique_floor_map
from contextlib import contextmanager


LOG_DIR = os.getenv('LOGFILE_DIR')
logfile_routing = os.path.join(LOG_DIR, "log_generate_route_network_dxf.log")
logging.basicConfig(filename=logfile_routing, level=logging.INFO, format='%(asctime)s %(message)s')



@contextmanager
def get_db_connection():
    db_user = os.getenv('PG_USER')
    db_name = os.getenv('PG_DB')
    db_host = os.getenv('PG_HOST')
    db_pass = os.getenv('PG_PASS')
    db_port = os.getenv('PG_PORT')

    conn_db = f"dbname={db_name} user={db_user} host={db_host} password={db_pass} port={db_port}"
    conn = psycopg2.connect(conn_db)
    try:
        yield conn
    finally:
        conn.close()


def node_working_networklines(schema, tablename, epsg=31259):
    # write doc string for this function
    """
    This function will take a table name and schema name and create a noded networklines table
    :param schema: schema name
    :param tablename: the networklines we edit manually to create the routing network.
    :param epsg: epsg code
    :return: Nones
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()

            temp_output_table = schema + "." + tablename + "_tmp_noded"
            temp_table_node = schema + ".temp_" + tablename
            temp_final_noded = schema + ".temp_" + tablename + "_tmp_noded"
            final_out = schema + "." + tablename + "_noded"

            if tablename in ['routing_networklines_z1', 'routing_networklines_z2', 'routing_networklines_z3',
                             'routing_networklines_z4', 'routing_networklines_z5', 'routing_networklines_zd', ]:
                sql_create_empty_table = f"""
                CREATE TABLE {final_out} AS TABLE {schema}.{tablename} WITH NO DATA;
                """
                cur.execute(sql_create_empty_table)
                conn.commit()
                return

            check = f"""SELECT CASE
                 WHEN EXISTS (SELECT * FROM {schema}.{tablename} LIMIT 1) THEN 1
                 ELSE 0
               END;"""
            cur.execute(check)
            x = cur.fetchone()
            if x[0] == 1:
                # everything good table exists just go go go
                pass
            else:
                logging.error("ERROR ..............  ERROR  .............")

            sql = f"""
                drop table if exists {temp_output_table};
                drop table if exists {temp_table_node};
                drop table if exists {temp_final_noded};
                drop table if exists {final_out};
        
                Select name, speed, source, target, cost, length, floor_num, floor_name,
                       network_type, access_type, st_setsrid((st_dump(geom)).geom, {epsg}) as temp_geom, fk_building_id
                    into {temp_table_node} from {schema}.{tablename};
        
        
                alter table {temp_table_node} add id serial;
                alter table {temp_table_node} add constraint {"temp_" + tablename}_pk primary key (id);
        
                SELECT AddGeometryColumn('{schema}', '{"temp_" + tablename}', 'geom', {epsg}, 'LINESTRING', 2);
        
                update {temp_table_node} set geom = temp_geom where 1=1;
        
                Alter table {temp_table_node} drop column temp_geom;
        
                select pgr_nodenetwork('{temp_table_node}', 0.1, 'id', 'geom', 'tmp_noded');
        
                SELECT id, name, speed, source, target, cost, length, floor_num, floor_name,
                     network_type, access_type, fk_building_id, geom
                   INTO {final_out} FROM
                    (select t.id, t.name, t.speed, t.source, t.target, t.cost, t.length, t.floor_num, t.floor_name,
                           t.network_type, t.access_type, t.fk_building_id, o.geom from {temp_table_node} t
                           join {temp_final_noded} o on o.old_id = t.id) as tmp;
        
               ALTER TABLE {final_out} RENAME COLUMN id TO old_id;
               ALTER TABLE {final_out} ADD COLUMN id SERIAL PRIMARY KEY;
               CREATE INDEX {final_out.split('.')[1:][0]}_geom_idx  ON {final_out} USING GIST (geom);
               CREATE INDEX {final_out.split('.')[1:][0]}_id_idx ON {final_out} (id);
        
            """
            cur.execute(sql)
            conn.commit()
            return {'success': 'node networklines created'}
    except Exception as e:
        logging.error(f"generating noded network failed {e}")
        return {'error': f'Failed to commit transaction: {e}'}


def drop_routing_views(floors):
    for floor in floors:
        floor = floor['letter'].lower()
        f = f"drop view if exists geodata.route_{floor.lower()}"
        execute_sql(f)


def delete_temp_tables():
    logging.info("deleting temp tables")
    for floor in unique_floor_map:

        floor_letter= floor['letter'].lower()

        drop_noded = f"""
            DROP TABLE IF EXISTS routing.routing_networklines_{floor_letter}_noded;
            DROP TABLE IF EXISTS routing.temp_routing_networklines_{floor_letter}_tmp_noded;
            
            DROP TABLE IF EXISTS routing.routing_networklines_{floor_letter}_noded_noded2;
            DROP TABLE IF EXISTS routing.temp_networklines_{floor_letter};
            DROP TABLE IF EXISTS routing.temp_routing_networklines_{floor_letter};
            DROP TABLE IF EXISTS routing.temp_routing_networklines_{floor_letter}_noded_tmp_noded;
            DROP TABLE IF EXISTS routing.temp_routing_networklines_{floor_letter}_noded_tmp_noded;
            DROP TABLE IF EXISTS routing.temp_routing_networklines_{floor_letter}_noded;
        """
        execute_sql(drop_noded)


def execute_sql(sql):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            return ({'success': 'success'})
    except Exception as e:
        return {'error': f'Failed to commit transaction: {e}'}

def update_table(schema, temp_net_table, floor_float, floor):

    noded_table_name = f"{schema}.routing_networklines_{floor}_noded"

    sql_setup = f"""
    DROP TABLE IF EXISTS {temp_net_table};
    SELECT id, ST_Force3D(ST_Transform(ST_Force2D(st_geometryN(geom, 1)),3857)) AS geom,
      network_type, cost::FLOAT, 0.0 AS reverse_cost, length, 0 AS source, 0 AS target, floor_name
      INTO {temp_net_table}
      FROM {noded_table_name};
    UPDATE {temp_net_table} SET geom=ST_Translate(ST_Force3DZ(geom),0,0,{floor_float}), 
                                length = ST_Length(geom),
                                id=id + {floor_float} + 100000.0, 
                                floor_name='{floor}';
    """
    execute_sql(sql_setup)
    execute_sql(f"UPDATE {temp_net_table} SET cost = 1 where cost=0 or cost IS NULL;")


def generate_networklines(schema, floormap):
    merged_network_lines = "geodata.networklines_3857"
    floors = [floor['letter'].lower() for floor in floormap]

    logging.info(f"GENERATING TEMP temp_networklines, for floors: {floors}")

    for floor in unique_floor_map:
        floor_float = floor['number']
        floor = floor['letter'].lower()
        temp_net_table = f"""{schema}.temp_networklines_{floor}"""

        update_table(schema, temp_net_table, floor_float, floor)
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
            OWNER to indrztu;
    """
    execute_sql(t1)

    logging.info(f"inserting data into floors {floors}")

    for floor in floors:
        floor_float = get_floor_float(floor)
        floor = floor.lower()
        src_networklines = f"""{schema}.temp_networklines_{floor}"""
        insert_sql_network = f"""INSERT INTO {merged_network_lines} (geom, length, network_type, 
                                        cost, reverse_cost, floor, floor_name)
                        SELECT geom, length, network_type, length*e0.cost as cost, 
                        0.0 AS reverse_cost, {floor_float} as floor, floor_name FROM {src_networklines} as e0;"""
        execute_sql(insert_sql_network)

    merge_it = f"""
    UPDATE {merged_network_lines} set reverse_cost = cost;
    CREATE INDEX geom_gist_index
       ON {merged_network_lines} USING gist (geom);
    CREATE INDEX id_idx
       ON {merged_network_lines} USING btree (id ASC NULLS LAST);
    CREATE INDEX network_layer_idx
      ON {merged_network_lines}
      USING hash
      (floor);
    SELECT Populate_Geometry_Columns('{merged_network_lines}'::regclass);
    UPDATE {merged_network_lines} SET geom=ST_AddPoint(geom,
      ST_EndPoint(ST_Translate(geom,0,0,1)))
      WHERE network_type IN (1, 2, 3);
    UPDATE {merged_network_lines} SET geom=ST_RemovePoint(geom,ST_NPoints(geom) - 2)
      WHERE network_type IN (1, 2, 3);
    ALTER TABLE {merged_network_lines} add column source integer;
    ALTER TABLE {merged_network_lines} add column target integer;"""

    logging.info("UDPATING merged networklines attributes source features")

    execute_sql(merge_it)

    logging.info("removing temp tables")

    for id, floor in enumerate(floors):
        floor = floor.lower()
        temp_net_table = f"""DROP TABLE IF EXISTS {schema}.temp_networklines_{floor}"""
        execute_sql(temp_net_table)

    last_work_sql = f"""
    DROP TABLE IF EXISTS {merged_network_lines}_vertices_pgr;
    SELECT public.pgr_createtopology3dIndrz('{merged_network_lines}', 0.01, 'geom', 'id', 'source', 'target', 'true', true);
    DELETE FROM {merged_network_lines} WHERE cost ISNULL OR length = 0;
    ALTER TABLE {merged_network_lines}_vertices_pgr OWNER TO "indrztu";
    """

    logging.info("creating topo 3d")

    execute_sql(last_work_sql)

    # conn.commit()
    return {"status": "success", "message": "new 3D networklines created"}


def generate_routing_network():
    drop_routing_views(unique_floor_map)
    delete_temp_tables()

    # wait 10 seconds
    time.sleep(10)

    logging.info("started generating noded networklines")
    for floor in unique_floor_map:
        floor_name = floor['letter'].lower()
        node_working_networklines("routing", f"routing_networklines_{floor_name}")

    logging.info("noded networklines generated, starting to generate networklines")

    generate_networklines("routing", unique_floor_map)

    delete_temp_tables()

    logging.info("DONE, networklines regenerated")
    return {"status": "success", "message": "networklines regenerated"}



if __name__ == '__main__':
    logging.info("started as SCRIPT generate routing")
    generate_routing_network()
    logging.info("finished as SCRIPT generate routing")