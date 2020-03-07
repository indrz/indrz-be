#!/bin/python
# coding: utf-8
import psycopg2
import time
from settings.secret_settings import db_pwd


table_abrev = ('eg00_', 'og01_', 'og02_', 'og03_')


# conn1 = psycopg2.connect(host='localhost', user='postgres', port='5434', password='air', database='wu_old_db')
# cur1 = conn1.cursor()
# cur2.execute("select building, geom from geodata.og01_umriss")
# f = cur2.fetchall()
# print(f)

# con_old_aau_db = psycopg2.connect(host='localhost', user='indrz-aau', port='5432', password='foo', database='indrzAauLiveOld')
# cur_old_aau_db = con_local_aau_db.cursor()


con_local_aau_db = psycopg2.connect(host='localhost', user='indrz-aau', port='5432', password=db_pwd, database='indrzAau')
cur_aau_local_db = con_local_aau_db.cursor()


def test_null(invalue):

    outval = None
    outval = invalue

    if invalue == "":
        outval = 'NULL'
    if invalue == " ":
        outval = 'NULL'
    if invalue == "\\None":
        outval = 'NULL'
    if invalue == 'None':
        outval = 'NULL'
    if invalue == None:
        outval = 'NULL'

    if outval == None:
        return outval
    else:
        if isinstance(invalue,str):
            return invalue.replace("'", "''")
        else:
            return invalue

def import_poi(floor_abr):

    """

    :param floor_abr: floor abreviation og02_  for example
    :return:
    """
    for building_abr, building_id in building_ids.items():
        if building_abr:
            floor_level_txt = floor_abr[3:4]
            print('now working on floor: ' + str(floor_level_txt))

            sel_spaces_new = """
                SELECT  poi.description_en, poi.cat_main_en, poi.cat_sub_en, poi.icon_name_css, poi.sort_order,
                    ST_MULTI(ST_TRANSFORM(poi.geom, 3857)) as geom, poi.aks_nummer
                FROM geodata.{0}poi AS poi,
                 geodata.buildings_buildingfloor AS floor
                 WHERE st_within(poi.geom,floor.geom)
                 AND floor.fk_building_id = {1}
                 AND floor.floor_num = {2}

                """.format(floor_abr, building_id, floor_level_txt)
            # print(sel_spaces_new)
            cur1.execute(sel_spaces_new)
            res = None
            res = cur1.fetchall()
            floor_level_txt = floor_abr[3:4]
            print("now on floor level: " + str(floor_level_txt))
            # print(len(res))
            # print(res)
            # print("the type is a " + str(type(res)))
            print("number of features to process: " + str(len(res)))
            if len(res) > 0:

                for r in res:


                    poi_name = test_null(r[0])

                    # print("room_name is : " + str(m_types))
                    m_geom = test_null(r[5])

                    poi_descript = test_null(r[6])


                    sel_building_floor_id = """SELECT id, floor_num, fk_building_id from django.buildings_buildingfloor
                              WHERE floor_num = {0} and fk_building_id = {1}""".format(floor_level_txt, building_id)
                    # print(sel_building_floor_id)

                    cur2.execute(sel_building_floor_id)
                    res_floor_id = cur2.fetchall()
                    # print(res_floor_id)

                    if res_floor_id:
                        # print(res_floor_id)
                        m_floor_id_value = res_floor_id[0][0]
                        # print(m_floor_id_value)
                        # print("FLOOR ID : " + str(m_floor_id_value))
                        if m_floor_id_value > 79:
                            print("we have a problem houston")

                        insert_state = """INSERT INTO django.poi_manager_poi (name, floor_num, fk_building_floor_id,
                                                      fk_campus_id, fk_building_id, category_id, geom, description)
                                    VALUES (\'{0}\', \'{1}\', {2}, {3},\'{4}\',{5},\'{6}\',\'{7}\'  )""".format(poi_name, floor_level_txt, m_floor_id_value,
                                                                               1, building_id, 12, m_geom, poi_descript)
                        print(insert_state)
                        cur2.execute(insert_state)
                        conn2.commit()

                print('done inserting on building id: ' + str(building_id))


aau_poi_data = [{"name_de":"Aula Buffet","id":47},
{"name_de":"Aula Cafe","id":49},
{"name_de":"B01","id":68},
{"name_de":"B03","id":68},
{"name_de":"B05","id":68},
{"name_de":"B06","id":68},
{"name_de":"B07","id":68},
{"name_de":"B08","id":68},
{"name_de":"B11","id":68},
{"name_de":"B12","id":68},
{"name_de":"Bäckerei Wienerroither","id":49},
{"name_de":"Bankomat (Aula)","id":63},
{"name_de":"BEH-WC","id":56},
{"name_de":"BH-WC","id":56},
{"name_de":"Bibliothek","id":8},
{"name_de":"Buchhandlung","id":8},
{"name_de":"Büro Kinder","id":68},
{"name_de":"Bushaltestelle Umkehrschleife","id":26},
{"name_de":"Bushaltestelle Universitätsstraße","id":26},
{"name_de":"Cafe","id":49},
{"name_de":"Cafeautomat Aula","id":48},
{"name_de":"Cafeautomat HS 1","id":48},
{"name_de":"Cafeautomat HS 7","id":48},
{"name_de":"Cafeautomat HS C","id":48},
{"name_de":"Cafeautomat I.1.43","id":48},
{"name_de":"Cafeautomat USI","id":48},
{"name_de":"Cafeautomat V.1.07","id":48},
{"name_de":"Campus-Radio","id":68},
{"name_de":"Clubhaus","id":68},
{"name_de":"Computer Gang Ost","id":35},
{"name_de":"Computer Gang West","id":35},
{"name_de":"Computerraum I.0.54","id":35},
{"name_de":"Computerraum I.0.54a","id":35},
{"name_de":"Computerraum V.1.02","id":35},
{"name_de":"Computerraum V.1.03","id":35},
{"name_de":"Computerraum Z.0.18","id":35},
{"name_de":"Computerraum Z.0.19","id":35},
{"name_de":"Dekanat","id":68},
{"name_de":"Druckerei","id":61},
{"name_de":"EDV","id":37},
{"name_de":"Eingang","id":13},
{"name_de":"Eingang 1 Lakeside B04","id":13},
{"name_de":"Eingang 2 Lakeside B02","id":13},
{"name_de":"Eingang 2 Lakeside B04","id":13},
{"name_de":"Eingang Lakeside B02","id":13},
{"name_de":"Eingang Mensa","id":13},
{"name_de":"Eingang Servicegebäude","id":13},
{"name_de":"Eingang Südtrakt","id":13},
{"name_de":"Elektrotankstelle Süd","id":68},
{"name_de":"Fahrradabstellplatz 1","id":17},
{"name_de":"Fahrradabstellplatz 2","id":17},
{"name_de":"Fahrradabstellplatz Nord 1","id":17},
{"name_de":"Fahrradabstellplatz Nord 2","id":17},
{"name_de":"Fahrradabstellplatz Nord 3","id":17},
{"name_de":"Fahrradabstellplatz Vorstufe","id":17},
{"name_de":"Getränkeautomat HS 1","id":48},
{"name_de":"Getränkeautomat HS 7","id":48},
{"name_de":"Getränkeautomat HS C","id":48},
{"name_de":"Getränkeautomat IQ","id":48},
{"name_de":"Getränkeautomat V.1.07","id":48},
{"name_de":"Haupteingang","id":13},
{"name_de":"IQ","id":49},
{"name_de":"Jobservice","id":37},
{"name_de":"Kassa","id":37},
{"name_de":"Kinderspielplatz","id":57},
{"name_de":"Kopierer","id":61},
{"name_de":"Kopierer Aula","id":61},
{"name_de":"Kopierer Bibliothek Ebene 2","id":61},
{"name_de":"Kopierer Bibliothek Ebene 3","id":61},
{"name_de":"Kopierer E.1.18","id":61},
{"name_de":"Kopierer HS 1","id":61},
{"name_de":"Kopierer HS 4","id":61},
{"name_de":"Kopierer HS 6","id":61},
{"name_de":"Kopierer Nordtrakt, Ebene 1","id":61},
{"name_de":"Kopierer Nordtrakt Ost, Ebene 2","id":61},
{"name_de":"Kopierer Nordtrakt West, Ebene 2","id":61},
{"name_de":"Kopiererraum Mathematik","id":61},
{"name_de":"Kopierer USI Ebene 2","id":61},
{"name_de":"Kopierer Vorstufengebäude","id":61},
{"name_de":"Kopierer Z.0.19","id":61},
{"name_de":"Kopierer ZID","id":61},
{"name_de":"Kopierraum Südtrakt","id":61},
{"name_de":"Lieferantenzufahrt","id":19},
{"name_de":"M O T School of Management, Organizational Development and Technology","id":30},
{"name_de":"ÖH ServiceCenter","id":30},
{"name_de":"ÖH Servicegebäude","id":30},
{"name_de":"Parkplatz_","id":6},
{"name_de":"Parkplatz Barrierefrei Ost","id":6},
{"name_de":"Parkplatz Barrierefrei Sued","id":6},
{"name_de":"Parkplatz Barrierefrei West","id":6},
{"name_de":"Parkplatz_Nord","id":6},
{"name_de":"Parkplatz_Ost","id":6},
{"name_de":"Parkplatz_Süd","id":6},
{"name_de":"Parkplatz_West","id":6},
{"name_de":"Parkscheinautomat Mensa","id":6},
{"name_de":"Parkscheinautomat, Nord","id":6},
{"name_de":"Parkscheinautomat Ost","id":6},
{"name_de":"Parkscheinautomat Süd","id":6},
{"name_de":"Parkscheinautomat, West 1","id":6},
{"name_de":"Parkscheinautomat, West 2","id":6},
{"name_de":"Portier","id":14},
{"name_de":"Post","id":68},
{"name_de":"Post (Uni)","id":68},
{"name_de":"Sekreteriat","id":30},
{"name_de":"Sekreteriat Lakeside","id":30},
{"name_de":"Sparkasse","id":30},
{"name_de":"Spinde","id":62},
{"name_de":"Städtische","id":30},
{"name_de":"Studentendorf","id":68},
{"name_de":"Studienabteilung","id":30},
{"name_de":"Studierenden-Arbeitsraum","id":68},
{"name_de":"Treffpunkt Aula","id":67},
{"name_de":"Treffpunkt Haupteingang","id":67},
{"name_de":"Treffpunkt Vorstufengebäude","id":67},
{"name_de":"Universitätsfreizeitzentrum UFZ","id":30},
{"name_de":"Uni Wirt","id":47},
{"name_de":"USI Eingang","id":13},
{"name_de":"USI Fußball","id":57},
{"name_de":"USI Gymnastik","id":57},
{"name_de":"USI Kletterwand","id":57},
{"name_de":"USI Kraftkammer","id":57},
{"name_de":"Vorstufengebäude Eingang","id":13},
{"name_de":"WASCHRAUM + WC","id":52},
{"name_de":"WC","id":52},
{"name_de":"WC Beh.","id":56},
{"name_de":"WCD","id":55},
{"name_de":"W CD","id":55},
{"name_de":"WC D","id":55},
{"name_de":"WC-D","id":55},
{"name_de":"WC Damen","id":55},
{"name_de":"WC-DAMEN","id":55},
{"name_de":"WC-DU-DAMEN","id":55},
{"name_de":"WC-DU-HERREN","id":54},
{"name_de":"WC-DUSCHE","id":52},
{"name_de":"WCH","id":56},
{"name_de":"W CH","id":56},
{"name_de":"WC H","id":56},
{"name_de":"WC-H","id":56},
{"name_de":"WC Herren","id":54},
{"name_de":"WC-HERREN","id":54},
{"name_de":"Wickelraum","id":18},
{"name_de":"Wickelraum Damen","id":70},
{"name_de":"Wickelraum E.0.24","id":70},
{"name_de":"Wickelraum Herren","id":70},
{"name_de":"Wickelraum K.0.06","id":70},
{"name_de":"Wickelraum M.1.25","id":70},
{"name_de":"Wickelraum T.0.02","id":70},
{"name_de":"Wickelraum V.1.10","id":70},
{"name_de":"Wickelraum Z.1.14e","id":70},
{"name_de":"WIFI","id":30},
{"name_de":"ZID Helpdesk","id":37}]


def assign_poi_cats():

    for item in aau_poi_data:

        poi_cat = item['id']
        poi_name = item['name_de']

        sel_poi_cats = """UPDATE django.poi_manager_poi set category_id = {0}
                                      WHERE name = \'{1}\'""".format(poi_cat, poi_name)

        print(sel_poi_cats)
        cur_aau_local_db.execute(sel_poi_cats)
        con_local_aau_db.commit()

# assign_poi_cats()


def enable_active_poicats():
    poi_cats_available = [
        {
            "category_id": 6
        },
        {
            "category_id": 8
        },
        {
            "category_id": 13
        },
        {
            "category_id": 14
        },
        {
            "category_id": 17
        },
        {
            "category_id": 18
        },
        {
            "category_id": 19
        },
        {
            "category_id": 26
        },
        {
            "category_id": 30
        },
        {
            "category_id": 35
        },
        {
            "category_id": 37
        },
        {
            "category_id": 47
        },
        {
            "category_id": 48
        },
        {
            "category_id": 49
        },
        {
            "category_id": 52
        },
        {
            "category_id": 54
        },
        {
            "category_id": 55
        },
        {
            "category_id": 56
        },
        {
            "category_id": 57
        },
        {
            "category_id": 61
        },
        {
            "category_id": 62
        },
        {
            "category_id": 63
        },
        {
            "category_id": 67
        },
        {
            "category_id": 68
        },
        {
            "category_id": 70
        }
    ]

    for poi in poi_cats_available:
        cat_id = poi['category_id']

        sel_poi_cats = """UPDATE django.poi_manager_poicategory set enabled = TRUE
                                      WHERE id = {0}""".format(cat_id)

        print(sel_poi_cats)
        cur_aau_local_db.execute(sel_poi_cats)
        con_local_aau_db.commit()

enable_active_poicats()
