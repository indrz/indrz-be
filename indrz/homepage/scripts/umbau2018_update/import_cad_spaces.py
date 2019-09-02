#!/bin/python
# coding: utf-8
from io import StringIO

import psycopg2
import time

# do a timestamp for being able to track execution time (if you want)
startscript = time.time()  # we will use this later

conn_indrzAau = psycopg2.connect(host='indrz.com', user='campusplan', port='5433', password='deineP7yee',
                                 database='indrzAau')
cur_indrzAau = conn_indrzAau.cursor()

# conn_dev_aau = psycopg2.connect(host='localhost', user='postgres', port='5432', password='air',
#                                 database='indrzAauLiveOld')
# cur_dev_aau = conn_dev_aau.cursor()

conn_prod_aau = psycopg2.connect(host='campusplan.aau.at', user='campusplan', port='5432', password='deineP7yee',
                                database='campusplan')
cur_prod_aau = conn_prod_aau.cursor()


# list of the floors to update
# floor_list = ('ug01_poi', 'eg00_poi', 'og01_poi', 'og02_poi', 'og03_poi', 'og04_poi', 'og05_poi', 'og06_poi' )
pg_schema = ('geodata')

table_abrev = ('e00_', 'e01_', 'e02_', 'e03_')
floor_nums = ("0", "1", "2", "3")

floor_values = ('poi', 'rooms', 'umriss', 'networklines', 'carto_lines', 'doors', 'furniture')
other_tables = ('parking_garage', 'raumlist_buchungsys', 'temp_wu_personal_data')
outdoor_tables = (
    'od_all_fill', 'od_all_polygons', 'od_baeume_linien', 'od_blindeleitlinie', 'od_fahrradstellplatz',
    'od_familie_linie',
    'od_orientierungselemente_linie', 'od_raucherzone', 'od_relax_area')
bibliothek_tables = ('bibliothek')

# query select array_to_json(array_agg(row_to_json(t))) from (select id, name from django.buildings_building) as t
building_ids = [{"id": 2, "name": "E"}, {"id": 3, "name": "B"}, {"id": 4, "name": "K"}, {"id": 5, "name": "T"},
                {"id": 6, "name": "V"}, {"id": 7, "name": "I"}, {"id": 8, "name": "Z"}, {"id": 9, "name": "B02"},
                {"id": 10, "name": "B04"}, {"id": 11, "name": "B09"}, {"id": 12, "name": "B10"},
                {"id": 13, "name": "B11"}, {"id": 14, "name": "M"}, {"id": 16, "name": "D4"}, {"id": 17, "name": "D10"},
                {"id": 18, "name": "D12"}, {"id": 19, "name": "D13"}, {"id": 20, "name": "D8"}]
space_type_id_map = {'Drucker': 69, }

rooms_cols = ('refname', 'room_name', 'room_number', 'building', 'floor', 'description', 'geom', 'building_number',
              'aks_nummer', 'entrance_poi_id', 'room_code', 'category_en')

indrz_spaces_cols = {'short_name': rooms_cols[1], 'geom': rooms_cols[6], 'room_number': rooms_cols[2],
                     'room_external_id': rooms_cols[8], 'room_number_sign': rooms_cols[10],
                     'fk_space_type_id': rooms_cols[11]}

sql_spatial_joing = """UPDATE geodata.e00_ply dst
                        SET text = src.text_ 
                        FROM geodata.e00_webanno src
                        WHERE ST_Intersects(src.geom, dst.geom);"""

def import_floor(floor_num, building_id, cur, conn):
    """
    Building must exist with id
    :param floor:
    :return:
    """
    # tbl_name = 'b01_floor'
    # tbl_name = 'b07_og01_floor'
    tbl_name = 'b08_og02_floor'

    sql_sel = """SELECT st_multi(geom) from temp.{0}""".format(tbl_name)

    cur.execute(sql_sel)
    r_floor = cur_indrzAau.fetchall()

    for res in r_floor:
        sql_insert = """INSERT INTO django.buildings_buildingfloor (fk_building_id, floor_num, geom, short_name) 
            VALUES ({0}, {1}, '{2}', '{3}')""".format(building_id, floor_num, res[0], 'E01')

        print(sql_insert)

        cur_prod_aau.execute(sql_insert)
    conn_prod_aau.commit()


# import_floor(1, 23, cur_indrzAau, conn_indrzAau)
# import_floor(2, 24, cur_indrzAau, conn_indrzAau)


def import_spaces(floor, cur, conn, building_id, floor_id):

    # tbl_name ='e0'+ str(floor) + '_spaces'
    # tbl_name = 'b01_spaces'
    # tbl_name = 'b07_og01_spaces'
    tbl_name = 'b08_og02_spaces'

    sql_sel = """SELECT st_multi(geom), room_code from temp.{0}""".format(tbl_name)

    cur.execute(sql_sel)
    results = cur.fetchall()

    for res in results:
        geom = res[0]
        room_code = res[1]

        sql_insert = """INSERT INTO django.buildings_buildingfloorspace (fk_building_id, floor_num, geom, room_code, fk_building_floor_id) 
            VALUES ({0}, {1}, '{2}','{3}', {4})""".format(building_id, floor, geom, room_code, floor_id)

        print(sql_insert)

        # print(sql_update)

        cur.execute(sql_insert)
    conn.commit()


# import_spaces(1, cur_indrzAau, conn_indrzAau, 23, 71)
# import_spaces(2, cur_indrzAau, conn_indrzAau, 24, 72)

def update_planlines(floor, building_id, cur, conn, floor_id):

    # tbl_names =['_doors', '_stairs_ramps', '_walls_wc']

    # tbl_names = ['b01_doors']
    tbl_names = ['b07_og01_furniture']
    # tbl_names = ['b08_og02_furniture']
    # sql_temp_floor = """select geom from temp.e00_floor where id = 6"""
    #
    # cur_indrzAau.execute(sql_temp_floor)
    # res_floors = cur_indrzAau.fetchall()

    for tbl_name in tbl_names:
        # cur_table = "e0" + str(floor) + tbl_name
        cur_table = tbl_name

        sql_sel = """SELECT type, st_multi(st_force2d(geom)) from temp.{0}""".format(cur_table)

        cur.execute(sql_sel)
        r_lines = cur_indrzAau.fetchall()

        for res in r_lines:

            sql_insert = """INSERT INTO django.buildings_buildingfloorplanline (fk_building_id, short_name, floor_num, geom, fk_building_floor_id) 
                VALUES ({0}, '{1}',{2}, '{3}', {4})""".format(building_id, res[0], floor, res[1], floor_id)

            # print(sql_update)

            cur_prod_aau.execute(sql_insert)
    conn_prod_aau.commit()


# update_planlines(3) # run this for each floor  update_planlines(1), update_planlines(0)
# update_planlines(1, 22, cur_indrzAau, conn_indrzAau)
update_planlines(1, 23, cur_indrzAau, conn_indrzAau, 71)
# update_planlines(2, 24, cur_indrzAau, conn_indrzAau, 72)


def update_space_type():

    sql_update = """update django.buildings_buildingfloorspace as s set short_name = r.raumbezeichnung from geodata.aaudata as r
     where upper(r.raumnr_schild) = upper(s.room_code);"""

    cur_prod_aau.execute(sql_update)
    conn_prod_aau.commit()

# update_space_type()

def set_space_types():
    current_types = [{"short_name": "Ablage", "id": 94}, {"short_name": "Abstellraum", "id": 94},
                     {"short_name": "Aggregatraum", "id": 94},
                     {"short_name": "Anlieferung", "id": 94},
                     {"short_name": "ANSCHLUSSCH.", "id": 94},
                     {"short_name": "ANSCHLUSSSCHACHT", "id": 94},
                     {"short_name": "AR", "id": 94},
                     {"short_name": "Archiv", "id": 94},
                     {"short_name": "ARCHIV/ADMIN", "id": 94},
                     {"short_name": "ARCHIV COMM", "id": 94},
                     {"short_name": "Archiv, Kopierraum", "id": 94},
                     {"short_name": "ASSEMBLING", "id": 94},
                     {"short_name": "Assist. Zimmer (Applied Mechatronics)", "id": 94},
                     {"short_name": "Assist. Zimmer VI", "id": 94},
                     {"short_name": "AUFENTHALT", "id": 94},
                     {"short_name": "Aufenthaltsraum", "id": 94},
                     {"short_name": "AUFENTHALTSRAUM", "id": 94},
                     {"short_name": "Aufzug (8 Pers./830 kg)", "id": 33},
                     {"short_name": "Aufzug (8 Pers./830kg)", "id": 33},
                     {"short_name": "Aula Vorstufe", "id": 44},
                     {"short_name": "Batterieraum", "id": 44},
                     {"short_name": "Begegnungsraum", "id": 63},
                     {"short_name": "Behinderten-WC", "id": 106},
                     {"short_name": "BEH-WC", "id": 106},
                     {"short_name": "BEH.WC", "id": 106},
                     {"short_name": "BEH. WC", "id": 106},
                     {"short_name": "Beratungsraum", "id": 63},
                     {"short_name": "Besprechung", "id": 63},
                     {"short_name": "BESPRECHUNG", "id": 63},
                     {"short_name": "Besprechungsraum", "id": 63},
                     {"short_name": "Besprechungsräum", "id": 63},
                     {"short_name": "Besprechungsräume", "id": 63},
                     {"short_name": "BETRIEBSRAT", "id": 94},
                     {"short_name": "BEWEGUNG", "id": 94},
                     {"short_name": "Bildwerferraum", "id": 94},
                     {"short_name": "BM-Zentrale", "id": 94},
                     {"short_name": "Boilerraum", "id": 94},
                     {"short_name": "Brücke", "id": 44},
                     {"short_name": "Bücherausgabestelle", "id": 94},
                     {"short_name": "Bücherlift", "id": 94},
                     {"short_name": "Buffetausgabe", "id": 94},
                     {"short_name": "BÜRO", "id": 63},
                     {"short_name": "BÜRO 2AP", "id": 63},
                     {"short_name": "Büroraum", "id": 63},
                     {"short_name": "BÜRORAUM", "id": 63},
                     {"short_name": "Büroraum (Uni Radio)", "id": 63},
                     {"short_name": "Bürotechnikraum", "id": 63},
                     {"short_name": "BÜRO TSG", "id": 63},
                     {"short_name": "Chefraum", "id": 63},
                     {"short_name": "COMM 1AP", "id": 20},
                     {"short_name": "COMM 2AP", "id": 20},
                     {"short_name": "Complab.+Werkstatt", "id": 20},
                     {"short_name": "Computerraum", "id": 20},
                     {"short_name": "DAT", "id": 94},
                     {"short_name": "Depot", "id": 94},
                     {"short_name": "Diplomanden-/Dissertantenraum", "id": 63},
                     {"short_name": "DissertantInnen", "id": 63},
                     {"short_name": "Dol.Kabine 1", "id": 94},
                     {"short_name": "Dol.Kabine 2", "id": 94},
                     {"short_name": "Dol.Kabine 3", "id": 94},
                     {"short_name": "Dolmetsch", "id": 94},
                     {"short_name": "DRUCKAUSGLEICHSKAMMER", "id": 24},
                     {"short_name": "Druckerei", "id": 24},
                     {"short_name": "DU", "id": 94},
                     {"short_name": "Dusche", "id": 78},
                     {"short_name": "DUSCHE", "id": 78},
                     {"short_name": "Duschen-Damen", "id": 78},
                     {"short_name": "Duschen-Herren", "id": 78},
                     {"short_name": "Dusche und WC", "id": 78},
                     {"short_name": "Duschvoraum-Herren", "id": 78},
                     {"short_name": "Duschvorraum-Damen", "id": 78},
                     {"short_name": "Duschvorraum-Herren", "id": 78},
                     {"short_name": "EDV-Raum", "id": 20},
                     {"short_name": "EDV Verteilerraum", "id": 20},
                     {"short_name": "EDV-Verteilerraum", "id": 20},
                     {"short_name": "E-Hauptverteiler", "id": 20},
                     {"short_name": "Eingangshalle", "id": 44},
                     {"short_name": "E-Install.Schacht", "id": 94},
                     {"short_name": "EMPFANG/ASSITENZ", "id": 94},
                     {"short_name": "E-Raum", "id": 94},
                     {"short_name": "E-RAUM", "id": 94},
                     {"short_name": "E-TECH.", "id": 94},
                     {"short_name": "E-Verteiler", "id": 94},
                     {"short_name": "E-VERTEILER", "id": 94},
                     {"short_name": "E-Verteilerraum", "id": 94},
                     {"short_name": "E-Verteilerraum/ Triebwerksraum", "id": 94},
                     {"short_name": "Fahrradabstellraum", "id": 94},
                     {"short_name": "Fernheizung", "id": 94},
                     {"short_name": "Fernleihe", "id": 94},
                     {"short_name": "Flur", "id": 44},
                     {"short_name": "Forschungmanagement", "id": 94},
                     {"short_name": "Foyer", "id": 44},
                     {"short_name": "Gaderobe-Damen", "id": 94},
                     {"short_name": "Gang", "id": 44},
                     {"short_name": "GANG", "id": 44},
                     {"short_name": "GANG B10", "id": 44},
                     {"short_name": "Gang/Vorraum", "id": 4},
                     {"short_name": "Garage", "id": 44},
                     {"short_name": "Garagen", "id": 94},
                     {"short_name": "Garderobe", "id": 44},
                     {"short_name": "GARDEROBE", "id": 44},
                     {"short_name": "Garderobe-Herren", "id": 44},
                     {"short_name": "Garderoben", "id": 44},
                     {"short_name": "Garderorbe", "id": 44},
                     {"short_name": "GASLAGER", "id": 94},
                     {"short_name": "Gemeinschaftsraum", "id": 94},
                     {"short_name": "Geräteraum", "id": 94},
                     {"short_name": "Geräteraum/HS4", "id": 94},
                     {"short_name": "Geschäftsführer", "id": 63},
                     {"short_name": "Getränkelager", "id": 94},
                     {"short_name": "GF 1", "id": 94},
                     {"short_name": "GF 2", "id": 94},
                     {"short_name": "Glashaus", "id": 94},
                     {"short_name": "GROSSRAUMBÜRO", "id": 94},
                     {"short_name": "Grundlagenlabor", "id": 50},
                     {"short_name": "Gruppenarbeitsraum", "id": 50},
                     {"short_name": "Gruppenraum", "id": 50},
                     {"short_name": "GRUPPENRAUM", "id": 50},
                     {"short_name": "Gymnastik, Tanzraum", "id": 94},
                     {"short_name": "HALLE", "id": 94},
                     {"short_name": "Hauptmagazin", "id": 94},
                     {"short_name": "HAUPTVERT.", "id": 94},
                     {"short_name": "Haustechnik", "id": 94},
                     {"short_name": "HAUSTECHNIK", "id": 94},
                     {"short_name": "Heizungs-/ Lüftunsraum", "id": 94},
                     {"short_name": "Heizungsraum", "id": 94},
                     {"short_name": "HEV", "id": 94},
                     {"short_name": "Hörsaal 1", "id": 6},
                     {"short_name": "Hörsaal 11", "id": 6},
                     {"short_name": "Hörsaal 2", "id": 6},
                     {"short_name": "Hörsaal 3", "id": 6},
                     {"short_name": "Hörsaal 4", "id": 6},
                     {"short_name": "Hörsaal 5", "id": 6},
                     {"short_name": "Hörsaal 6", "id": 6},
                     {"short_name": "Hörsaal 7", "id": 6},
                     {"short_name": "Hörsaal 8", "id": 6},
                     {"short_name": "Hörsaal 9", "id": 6},
                     {"short_name": "Hörsaal A", "id": 6},
                     {"short_name": "Hörsaal B", "id": 6},
                     {"short_name": "Hörsaal C", "id": 6},
                     {"short_name": "ICT-Labor IST- VI", "id": 94},
                     {"short_name": "Installationsschacht", "id": 94},
                     {"short_name": "INSTALLATIONSSCHACHT", "id": 94},
                     {"short_name": "Install. Schacht", "id": 94},
                     {"short_name": "Karl-Popper-Sammlung", "id": 94},
                     {"short_name": "Katalograum", "id": 94},
                     {"short_name": "Kellerraum 1", "id": 94},
                     {"short_name": "Kellerraum 2", "id": 94},
                     {"short_name": "Kinderbetreuung", "id": 94},
                     {"short_name": "Kommunikationszentrale", "id": 94},
                     {"short_name": "KOPIEREN", "id": 24},
                     {"short_name": "Kopierraum", "id": 24},
                     {"short_name": "Korridor", "id": 44},
                     {"short_name": "Krafttrainingsraum", "id": 94},
                     {"short_name": "Küche", "id": 94},
                     {"short_name": "KÜCHE", "id": 94},
                     {"short_name": "Küchenchef", "id": 94},
                     {"short_name": "Kühlzellen", "id": 94},
                     {"short_name": "Labor", "id": 50},
                     {"short_name": "Labor ", "id": 50},
                     {"short_name": "Labor 1", "id": 50},
                     {"short_name": "Labor 2", "id": 50},
                     {"short_name": "Labor 3", "id": 50},
                     {"short_name": "Labor AM", "id": 50},
                     {"short_name": "Labor, Embedded Systems", "id": 50},
                     {"short_name": "Labor, Pervasive Computing", "id": 50},
                     {"short_name": "Lackiererei", "id": 94},
                     {"short_name": "Lager", "id": 94},
                     {"short_name": "LAGER", "id": 94},
                     {"short_name": "Lager Cafe", "id": 94},
                     {"short_name": "Lagerraum", "id": 94},
                     {"short_name": "LAN", "id": 94},
                     {"short_name": "Leergut", "id": 94},
                     {"short_name": "Leihstelle", "id": 94},
                     {"short_name": "Lektorenraum", "id": 94},
                     {"short_name": "Leseraum", "id": 94},
                     {"short_name": "Lesesaal", "id": 94},
                     {"short_name": "Lift", "id": 94},
                     {"short_name": "LIFTGRUBE", "id": 94},
                     {"short_name": "LOGGIA", "id": 94},
                     {"short_name": "Lüftung", "id": 94},
                     {"short_name": "Lüftung/ Lager", "id": 94},
                     {"short_name": "Lüftungszentrale", "id": 94},
                     {"short_name": "Magazin", "id": 94},
                     {"short_name": "Mediathek", "id": 94},
                     {"short_name": "Meditationsraum", "id": 94},
                     {"short_name": "MEETINGRAUM", "id": 94},
                     {"short_name": "MEHRZWECKR.", "id": 94},
                     {"short_name": "Mensa", "id": 94},
                     {"short_name": "Müll", "id": 94},
                     {"short_name": "MÜLL", "id": 94},
                     {"short_name": "Müllcontainer", "id": 94},
                     {"short_name": "MÜLLRAUM", "id": 94},
                     {"short_name": "Naßmüll", "id": 94},
                     {"short_name": "Nebenr. zu Lüftungszentrale HS C", "id": 94},
                     {"short_name": "None", "id": 94},
                     {"short_name": "NOTSTROMAGGREGAT", "id": 94},
                     {"short_name": "OFFICE", "id": 94},
                     {"short_name": "OPS", "id": 94},
                     {"short_name": "Periodikamagazin", "id": 94},
                     {"short_name": "Personalraum", "id": 94},
                     {"short_name": "Personalraum ", "id": 94},
                     {"short_name": "Personalraum (Applied Mechatronics)", "id": 94},
                     {"short_name": "Personalraum (Applied Mechatronics u. Controll Messurement)", "id": 94},
                     {"short_name": "Personalraum Assist. (Control Messurement)", "id": 94},
                     {"short_name": "PERSONAL/UMKLEIDE", "id": 94},
                     {"short_name": "Pesonalraum", "id": 94},
                     {"short_name": "Podest", "id": 94},
                     {"short_name": "Portierstelle", "id": 94},
                     {"short_name": "Poststelle", "id": 94},
                     {"short_name": "PR", "id": 94},
                     {"short_name": "PRINT", "id": 94},
                     {"short_name": "Prof. Raum (Control Messurement)", "id": 94},
                     {"short_name": "Prof. Zimmer VI", "id": 94},
                     {"short_name": "Projektionsraum", "id": 94},
                     {"short_name": "Projektraum", "id": 94},
                     {"short_name": "PROJEKTRAUM", "id": 94},
                     {"short_name": "PR/SERVER", "id": 94},
                     {"short_name": "PUTZR.", "id": 94},
                     {"short_name": "Putzraum", "id": 94},
                     {"short_name": "ramp", "id": 94},
                     {"short_name": "RAUCHER", "id": 94},
                     {"short_name": "Reflektorium", "id": 94},
                     {"short_name": "Regieraum", "id": 94},
                     {"short_name": "RZ 1", "id": 94},
                     {"short_name": "RZ 2", "id": 94},
                     {"short_name": "RZ 3", "id": 94},
                     {"short_name": "SALES", "id": 94},
                     {"short_name": "SANITÄR", "id": 94},
                     {"short_name": "Schalterraum", "id": 94},
                     {"short_name": "Schleuse", "id": 94},
                     {"short_name": "Schlosserei", "id": 94},
                     {"short_name": "Schnitt 1", "id": 94},
                     {"short_name": "Schnitt 2", "id": 94},
                     {"short_name": "Schwachstrom", "id": 94},
                     {"short_name": "Sehbehindertenraum", "id": 94},
                     {"short_name": "Sekretariat (Applied Mechatronics)", "id": 94},
                     {"short_name": "Sekretariat VI + Control", "id": 94},
                     {"short_name": "Sekreteriat", "id": 94},
                     {"short_name": "Selbstbedienung", "id": 94},
                     {"short_name": "Self Access Center", "id": 94},
                     {"short_name": "Seminar-Demoraum", "id": 94},
                     {"short_name": "Seminarraum", "id": 94},
                     {"short_name": "SERVER/PR", "id": 94},
                     {"short_name": "Serverraum", "id": 94},
                     {"short_name": "Service", "id": 94},
                     {"short_name": "Sitzungszimmer", "id": 94},
                     {"short_name": "SOL", "id": 94},
                     {"short_name": "SONDERMIETER", "id": 94},
                     {"short_name": "Sondersammlung", "id": 94},
                     {"short_name": "Sozialraum", "id": 94},
                     {"short_name": "SOZIALRAUM", "id": 94},
                     {"short_name": "SR2", "id": 94},
                     {"short_name": "STGH", "id": 79},
                     {"short_name": "STGH.", "id": 79},
                     {"short_name": "Stiege", "id": 79},
                     {"short_name": "Stiegen", "id": 79},
                     {"short_name": "Stiegenhaus", "id": 79},
                     {"short_name": "Studentenraum", "id": 94},
                     {"short_name": "Tankraum", "id": 94},
                     {"short_name": "TANKRAUM", "id": 94},
                     {"short_name": "Technik", "id": 94},
                     {"short_name": "Techniker VI", "id": 94},
                     {"short_name": "Technikraum", "id": 94},
                     {"short_name": "Technikterrasse", "id": 94},
                     {"short_name": "TECHNIK - TERRASSE", "id": 94},
                     {"short_name": "TECHNIK (TERRASSE)", "id": 94},
                     {"short_name": "TEEK./SOZIALR.", "id": 94},
                     {"short_name": "Teeküche", "id": 94},
                     {"short_name": "TEEKÜCHE", "id": 94},
                     {"short_name": "Telefonzentrale", "id": 94},
                     {"short_name": "Tel.Vermittlung", "id": 94},
                     {"short_name": "Terasse", "id": 94},
                     {"short_name": "TERRASSE", "id": 94},
                     {"short_name": "Testraum", "id": 94},
                     {"short_name": "Tischlerei", "id": 94},
                     {"short_name": "TRAFOR.", "id": 94},
                     {"short_name": "Traforaum", "id": 94},
                     {"short_name": "TRAFORAUM", "id": 94},
                     {"short_name": "Trafostation STW-K", "id": 94},
                     {"short_name": "TRANSFERRAUM", "id": 94},
                     {"short_name": "Trockenmüll", "id": 94},
                     {"short_name": "Turnhalle", "id": 94},
                     {"short_name": "Überdachter Innenhof", "id": 94},
                     {"short_name": "Umformerraum", "id": 94},
                     {"short_name": "Umkleide-Damen", "id": 94},
                     {"short_name": "Umkleide-Herren", "id": 94},
                     {"short_name": "unknown", "id": 94},
                     {"short_name": "unkown", "id": 94},
                     {"short_name": "Unterrichtsraum", "id": 94},
                     {"short_name": "Usability Lab", "id": 94},
                     {"short_name": "USV", "id": 94},
                     {"short_name": "USV 1", "id": 94},
                     {"short_name": "USV 2", "id": 94},
                     {"short_name": "USV 3", "id": 94},
                     {"short_name": "USV-Raum", "id": 94},
                     {"short_name": "Veranstaltungssaal", "id": 94},
                     {"short_name": "Verb.Gang", "id": 94},
                     {"short_name": "VERBIND.", "id": 94},
                     {"short_name": "Verkaufsraum", "id": 94},
                     {"short_name": "Verteilerraum", "id": 94},
                     {"short_name": "Vorbereitung", "id": 94},
                     {"short_name": "Vorbereitungsraum", "id": 94},
                     {"short_name": "Vorführraum", "id": 94},
                     {"short_name": "VORR.", "id": 44},
                     {"short_name": "Vorraum", "id": 44},
                     {"short_name": "Vorraum ", "id": 44},
                     {"short_name": "VR", "id": 44},
                     {"short_name": "Warenübernahme", "id": 94},
                     {"short_name": "WARTEN", "id": 44},
                     {"short_name": "Warteraum", "id": 44},
                     {"short_name": "Waschraum", "id": 91},
                     {"short_name": "Waschraum Damen", "id": 91},
                     {"short_name": "Waschraum Herren", "id": 91},
                     {"short_name": "wc", "id": 91},
                     {"short_name": "WC", "id": 91},
                     {"short_name": "WC Behinderte", "id": 106},
                     {"short_name": "WC-D", "id": 105},
                     {"short_name": "WC DA", "id": 105},
                     {"short_name": "WC Damen", "id": 105},
                     {"short_name": "WC-Damen", "id": 105},
                     {"short_name": "WC Damen Vorraum", "id": 105},
                     {"short_name": "WC Dusche", "id": 78},
                     {"short_name": "WC-H", "id": 104},
                     {"short_name": "WC HE", "id": 104},
                     {"short_name": "WC Herren", "id": 104},
                     {"short_name": "WC-Herren", "id": 104},
                     {"short_name": "WC Herren Vorraum", "id": 104},
                     {"short_name": "Werkstatt", "id": 94},
                     {"short_name": "Werkstätte", "id": 94},
                     {"short_name": "Wickelraum", "id": 94},
                     {"short_name": "Windfang", "id": 44},
                     {"short_name": "WIRTSCHAFTSR.", "id": 94},
                     {"short_name": "WR/WC", "id": 91},
                     {"short_name": "Zeitschriftenraum, Besprechungsraum", "id": 94},
                     {"short_name": "ZL-Trafo", "id": 94},
                     ]


    for item in current_types:
        spacetype_id = item['id']
        space_name = item['short_name']

        sel_spaces = """UPDATE django.buildings_buildingfloorspace set space_type_id = {0}
                                      WHERE short_name ilike \'%{1}%\'""".format(spacetype_id, space_name)


        cur_prod_aau.execute(sel_spaces)
        conn_prod_aau.commit()
# set_space_types()
# conn.commit()
# cur.close()
# conn.close()

endscript = time.time()
endtime = endscript - startscript
print('script run in ' + str(endscript - startscript) + ' seconds or ' + '\n'
      + str((endscript - startscript) * 1000) + ' miliseconds')



