import psycopg2
import os

db_user = os.getenv('PG_USER')
db_name = os.getenv('PG_DB')
db_host = os.getenv('PG_HOST')
db_pass = os.getenv('PG_PASS')
db_port = os.getenv('PG_PORT')


con_local = f"dbname=indrztu user=indrztu host=indrz_db password=air port=5432"
con_prod = f"dbname=indrztu user=tu host=tuw-maps.tuwien.ac.at password=air port=5433"


conn = psycopg2.connect(con_prod)
cur = conn.cursor()

unique_floor_map = [    {'name': 'u4_0', 'number': -4.0, 'letter': 'U4'},
                        {'name': 'u3_0', 'number': -3.0, 'letter': 'U3'},
                        {'name': 'u2_0', 'number': -2.0, 'letter': 'U2'},
                        {'name': 'u1_5', 'number': -1.5, 'letter': 'ZU'},
                        {'name': 'u1_0', 'number': -1.0, 'letter': 'U1'},
                        {'name': 'u0_5', 'number': -0.5, 'letter': 'SO'},
                        {'name': '0_0', 'number': 0.0, 'letter': 'EG'},
                        {'name': '0_5', 'number': 0.5, 'letter': 'ZE'},
                        {'name': '1_0', 'number': 1.0, 'letter': '01'},
                        {'name': '1_5', 'number': 1.5, 'letter': 'Z1'},
                        {'name': '2_0', 'number': 2.0, 'letter': '02'},
                        {'name': '2_5', 'number': 2.5, 'letter': 'Z2'},
                        {'name': '3_0', 'number': 3.0, 'letter': '03'},
                        {'name': '3_5', 'number': 3.5, 'letter': 'Z3'},
                        {'name': '4_0', 'number': 4.0, 'letter': '04'},
                        {'name': '4_5', 'number': 4.5, 'letter': 'Z4'},
                        {'name': '5_0', 'number': 5.0, 'letter': '05'},
                        {'name': '5_5', 'number': 5.5, 'letter': 'Z5'},
                        {'name': '6_0', 'number': 6.0, 'letter': '06'},
                        {'name': '7_0', 'number': 7.0, 'letter': '07'},
                        {'name': '8_0', 'number': 8.0, 'letter': '08'},
                        {'name': '9_0', 'number': 9.0, 'letter': '09'},
                        {'name': '10_0', 'number': 10.0, 'letter': '10'},
                        {'name': '11_0', 'number': 11.0, 'letter': '11'},
                        {'name': '12_0', 'number': 12.0, 'letter': '12'},
                        {'name': '7777_0', 'number': 7777, 'letter': 'ZD'},
                        {'name': '9999_0', 'number': 9999, 'letter': 'DG'}]


def check_connectivity(lowerfloor, upperfloor):
    """
    Check for connectivity in the routing networks
    lowerfloor geodata.routing_networklines_ug01
    upperfloor geodata.routing_networklines_ug02
    """
    print("lower floor: ", lowerfloor)

    cur.execute(f"""select id from {lowerfloor} where network_type in (2);""")


    count_lower = cur.fetchall()


    # print("total ids in lower layer ", len(count_lower))
    #
    # cur.execute(f""" select count(id) from {upperfloor} where network_type in (1,2);""")
    # count_upper = cur.fetchall()

    # extra_sql = """
    # select id from routing.routing_networklines_ug02 where network_type in (1,2) order by id asc;
    #
    # -- check if floor change works
    # select distinct on (endug03.id) endug03.id, endug03.geom, endug03.network_type from routing.routing_networklines_ug03 endug03
    #     join routing.routing_networklines_ug02 start02
    #                 on st_intersects(endug03.geom, start02.geom)
    #                 where endug03.network_type in (1,2);"""


    # sql_join_count = f"""
    # select distinct endline.id from {lowerfloor} endline
    # join {upperfloor} startline
    #             on st_intersects(st_endpoint(endline.geom), st_startpoint(startline.geom))
    #             where endline.network_type in (2);
    #             """

    ne = f"""
        SELECT
      low_floor.id as eg_id
    FROM {lowerfloor} AS low_floor
    LEFT JOIN {upperfloor} AS up_floor
    
    
select id,st_endpoint((ST_Dump(ST_UnaryUnion(ST_Node(geom)))).geom) as geom, network_type from routing.routing_networklines_eg
where network_type = 2;
    
    ON ST_intersects(st_endpoint((ST_Dump(ST_UnaryUnion(ST_Node(low_floor.geom)))).geom), st_startpoint((ST_Dump(ST_UnaryUnion(ST_Node(up_floor.geom)))).geom))
    WHERE up_floor.network_type in (2)
    AND low_floor.network_type in (2);

    """

    # print(sql_join_count)
    cur.execute(ne)
    join_count = cur.fetchall()
    # print("upper count, ", join_count)

    errors_tofix = len(count_lower) - len(join_count)

    if len(join_count) == len(count_lower):
        # print(f"we are good for lower {lowerfloor[-8:]} join count: {len(join_count)} and count lower : {len(count_lower)}")
        pass
    else:
        print(f"--- TOTAL  {errors_tofix} errors to fix join count: {len(join_count)} and count lower : {len(count_lower)} , ids of {lowerfloor}")

        ids_to_fix = set(count_lower).difference(set(join_count))# nt))
        print("ids to fix: ", sorted(ids_to_fix))
        # print("ids of all lines that are good and intersect ", sorted(join_count))

        # print(f"DIFF floor {lowerfloor[-8:]} ids are:", sorted(set(count_lower).difference(set(join_count))))


    return {"floor": lowerfloor, "total": errors_tofix}


def list_segs_not_connected(floor):
    '''
    check one floor for any network lines that don't intersect any other network line for same floor
    example list_segs_not_connected('01')

    NOTE you can use the same query in QGIS to visualize where the problems are located
    '''
    layer = f"routing.routing_networklines_{floor}_noded"
    s = f"""
    SELECT id, geom FROM {layer} a
        WHERE NOT EXISTS 
         (SELECT 1 FROM {layer} b 
          WHERE a.id != b.id
          AND   ST_Intersects(a.geom, b.geom))
      """
    cur.execute(s)
    res = cur.fetchall()
    print([str(x[0]) for x in res])
    print("total segs not connected", len([str(x) for x in res]))


if __name__ == '__main__':

    # floor_names = (['u4', 'u3'],['u3', 'u2'],['u2', 'u1'],['u1', 'eg'],['eg', '01'],['01', '02'],['03', '04'],
    #                ['04', '05'], ['06', '07'], ['07', '08'], ['09', '10'],)

    floor_names = (['eg', '01'],)

    total_lower_errors = []

    for floor_pair in floor_names:
        print(f"------------ {floor_pair} -------------------")
        errors_tofix = check_connectivity(f"routing.routing_networklines_{floor_pair[0]}", f"routing.routing_networklines_{floor_pair[1]}")
        total_lower_errors.append(errors_tofix)

    # list_segs_not_connected('eg')


    print("total errors: ", sum([x['total'] for x in total_lower_errors]))

