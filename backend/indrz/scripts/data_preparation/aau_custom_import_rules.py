def special_room_import_rule(cur, conn):
    print("running sql special ")
    sql_set_to_hallway = """update django.buildings_buildingfloorspace set space_type_id = 44 
                                where room_code = 'S.1.H';"""
    cur.execute(sql_set_to_hallway)


    # Set large areas with no room code set color to white
    sql_fix_01_to_white = """update django.buildings_buildingfloorspace set space_type_id = 44
                            where st_area(geom) > 1695 
                            and tags[1]='Campus_Z_S_L_N_V_OG01' 
                            or room_code = 'V.1.0'
                            ;"""

    sql_fix_02_to_white = """update django.buildings_buildingfloorspace set space_type_id = 44
                             where st_area(geom) > 1400 and floor_num = 2.0
                            and tags[1]='Campus_Z_S_L_N_V_OG02'
                            and short_name is null;
                            ;"""

    sql_fix_03_to_white = """update django.buildings_buildingfloorspace set space_type_id = 44
                             where floor_num = 0.0
                            and room_code in ('B11a.0.0.0','B11a.0.0.1', 'B11a.0.1.1','B11a.0.1.2', 'B11a.0.1.6', 
                            'B11b.0.0.10', 'B11b.0.0.2', 'B11b.0.0.3', 'B11c.0.0.1')
                            and short_name is null;
                            ;"""

    sql_fix_04_white = """update django.buildings_buildingfloorspace set space_type_id = 44
                             where room_code in ('B11a.1.0.901','B11b.1.1.1','B11b.1.1.9','B11b.1.0.1','B11c.1.S4','B12a.1.0.1',
                                                'B12a.1.1.1','B12a.1.1.13','B12a.1.1.8','B12a.1.2.1','B12b.1.0.1','B12b.1.1.1',
                                                'B12b.1.3.0','B12b.1.3.1','B12c.1.1.1a','B12c.1.1.1b','B12c.1.1.1c', 'B11a.1.1.1',
                                                'B11b.2.1.1','B11a.2.0.1', 'B12c.2.1.1','B12b.2.1.1', 'B12b.2.0.0','B04.1.107',
                                                'B01.1.606','B07.1.101','B07.1.217','B07.1.101','B08.2.008')
                            and short_name is null;"""

    cur.execute(sql_fix_01_to_white)
    cur.execute(sql_fix_02_to_white)
    cur.execute(sql_fix_03_to_white)
    cur.execute(sql_fix_04_white)

    # Floor OG01 set to lift
    sql_fix_to_lift = """update django.buildings_buildingfloorspace set space_type_id = 33
                            where room_code in('N.1.44a','B01.1.001','B01.1.001');"""
    cur.execute(sql_fix_to_lift)

    # WC
    sql_fix_01_wc = """update django.buildings_buildingfloorspace set space_type_id = 91
                             where room_code in ('B11b.0.0.8', 'B11b.0.0.7','B11b.0.0.6','B11b.0.0.5','B11b.0.0.4',
                            'B11a.0.1.18','B11a.0.1.15','B11a.0.1.16','B11a.0.1.17','B11a.1.1.8','B11a.1.1.7',
                            'B11a.1.1.8', 'B11a.1.17', 'B12a.1.1.14','B07.1.002','B07.1.003')
                            and short_name is null;
                            ;"""

    cur.execute(sql_fix_01_wc)

    # stairs
    sql_fix_01_stairs = """update django.buildings_buildingfloorspace set space_type_id = 79
                             where room_code in ('B12a.2.0.0','B11a.2.0.0','B12b.2.0.0', 'B12c.2.0.0',
                             'B11a.1.0.0','B12b.1.0.0','B12c.1.0.0','B11c.1.0.0', 'B11a.1.0.0','B07.1.001','B04.1.006',
                                                'B04.1.001')
                            and short_name is null;"""

    cur.execute(sql_fix_01_stairs)

    conn.commit()