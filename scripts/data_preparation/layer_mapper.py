import os
from django.contrib.gis.gdal import DataSource, SpatialReference
import psycopg2

from pathlib import Path


db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASSWORD')

con_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass}"
ogr_db_con = f"PG: host={db_host} user={db_user} dbname={db_name} password={db_pass}"

conn = psycopg2.connect(con_string)
cur = conn.cursor()

# from django.contrib.gis.utils import LayerMapping
# from indrz.models import Buildingfloor, BuildingFloorPlanLine, BuildingFloorSpace, Building

# https://docs.djangoproject.com/en/2.2/ref/contrib/gis/gdal/#django.contrib.gis.gdal.Layer


# https://docs.djangoproject.com/en/2.2/ref/contrib/gis/layermapping/
# mapping = {'name' : 'str', # The 'name' model field maps to the 'str' layer field.
#                'poly' : 'POLYGON', # For geometry fields use OGC name.
#                } # The mapping is a dictionary#
# lm = LayerMapping(Buildingfloor, 'test_poly.shp', mapping)
# lm.save(verbose=True) # Save the layermap, imports the data.

# austria_gk_mk34 = SpatialReference(31249)

# database = 'indrztudata'
# usr = 'postgres'
# pw = 'air'
# table = 'test'

# connectionString = "PG:dbname='%s' user='%s' password='%s'" % (database,usr,pw)
# ogrds = ogr.Open(connectionString)

linefeatures = [
{'layer': 'E_S29', 'type': 'sink'},
{'layer': 'O_F49', 'type': 'window'},
{'layer': 'M_V29 (Fassadenverkleidung)', 'type': 'window'},
{'layer': 'S_29', 'type': 'stairs'},
{'layer': 'S_27', 'type':'stairs'},
{'layer': 'M_A29', 'type':'outer-wall'},
{'layer': 'A_A29_VER', 'type':'outer-wall'},
{'layer': 'OUT26', 'type':'outer-wall'},
{'layer': 'M_L29', 'type':'inner-wall'},
{'layer': 'M_Z29', 'type':'inner-wall'},
{'layer': 'A2-TUER-SYM050', 'type': 'door'},
{'layer': 'O_T49', 'type': 'door'},
{'layer': 'O_T29', 'type': 'door'}]

cad_layer_names = [x['layer'] for x in linefeatures]

cad_spaces_names = ['Z_009',]
cad_label_layers = ['B_127N', 'B_227Z','XRNR0', 'XRNR', 'GUT_RAUMSTEMPEL']
cad_floor_umriss = ['B_227IDTR']


def group_floor(name):
    """
    All data with the same floor number should be stored together

    """
    text = ""
    unique_floor_names = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'DG', 'EG', 'SO', 'U1', 'U2', 'U3', 'U4', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'ZD', 'ZE', 'ZU']
    

def read_dxf(name):

    ds = DataSource(name)
    print("num of layers is ", ds.layer_count)
    lyr = ds[0]

    
    print("layer fiels are:", lyr.fields)
    print("number of features: ", lyr.num_feat)

    field_types = [ft.__name__ for ft in lyr.field_types]
    print("lyr field types are , ", field_types)
    print("lyr field widths are: ", lyr.field_widths)


    feat_names = [feat.get('Layer') for feat in lyr]


    # for feat in lyr:

    #     print(feat.fid, feat.geom.geom_type, feat.geom, feat.fields, feat.layer_name) #0 LINESTRING (7540750437 340250.600061613,752337.50231658 340250.678862686) ['Layer', 'SubClasses', 'ExtendedEntity', 'Linetype', 'EntityHandle', 'Text'] entities

    #     print("feat is ", feat, "some value", feat['Layer'].value, " text value is:  ", feat['Text'].value)

    for field in lyr.fields:
        print("field is: ", field)


    dxf_layer_names_unique = set()

    dxf_layer_names = lyr.get_fields('Layer')
    for dxf_layer_name in dxf_layer_names:
        dxf_layer_names_unique.add(dxf_layer_name)


    print("cad layer names we look for: ", cad_layer_names)

    for linefeature in linefeatures:
        if linefeature['layer'] in dxf_layer_names_unique:
            # this means this layer is in the dxf file and in our list types we need oh goodie goo
            print("linefeat type is: ", linefeature['type'])


    print("count layers ", len(dxf_layer_names_unique), "dxf-layer names:  ", dxf_layer_names_unique)


    # for feat in lyr:
    #     x = feat.get('SubClasses')
    #     if x == "AcDbEntity:AcDbText:AcDbAttributeDefinition": #AcDbEntity:AcDbMText    AcDbEntity:AcDbBlockReference   AcDbEntity:AcDbText:AcDbAttributeDefinition
    #         print("layer name is ", feat.get('Layer'))
    #         print(x)
        # print(x)
    geos = [pt.json for pt in lyr.get_geoms()]

# print(geos)
# read_dxf('BA_01_IP_032019-2013.dxf')


def import_dxf_files():

    dxf_file_paths = get_dxf_files('Getreidemarkt',floor=None)
    myset = set()
    for dxf_file in dxf_file_paths:
        floor_int = get_floor_int(dxf_file)
        floor_table_name = create_floor_group_name(floor_int)

        dxf_floor = dxf_file.stem.split('_')[1]
        dxf_trak = dxf_file.stem.split('_')[0]
        line_table_name = "indrz_lines_" + str(dxf_floor)
        space_table_name = "indrz_spaces_" + str(dxf_floor)
        labels_table_name = "indrz_labels_" + str(dxf_floor)


        ds = DataSource(str(dxf_file))
        lyr = ds[0]

        # print("FIELDS INCLUDE: ", lyr.fields)
        

        # only do floor 01
        print("now on dxf file: ", dxf_file, "   TOTAL FEATURES: ", lyr.num_feat)
        
        for feat in lyr:
            # ['Layer', 'SubClasses', 'ExtendedEntity', 'Linetype', 'EntityHandle', 'Text']
            dxf_layer_name = feat.get('Layer')
            dxf_text = feat.get('Text')
            dxf_ext_entitiy = feat.get('ExtendedEntity')
            dxf_linetype = feat.get('Linetype')
            # myset.add(dxf_linetype)

            if dxf_layer_name in cad_layer_names:
                line_geom_types = ['MultiLineString', 'LineString25D', 'LineString', 'MultiLineString25D']
                if feat.geom.geom_type in line_geom_types:

                    sql_insert = f"INSERT INTO geodata.{line_table_name} (geom, short_name, long_name, floor_num) VALUES (ST_Force2d(ST_MULTI(ST_GeomFromText('{feat.geom}',31259))), '{dxf_trak}-{dxf_layer_name}', '{dxf_text}', {floor_int});"
                    # print("my insert is: ", sql_insert)
                    cur.execute(sql_insert)
                    conn.commit()

            # if dxf_layer_name in cad_spaces_names:
            #     if feat.geom.num_points >= 4:
            #         sql_insert = f"INSERT INTO geodata.{space_table_name} (geom, short_name, long_name, floor_num) VALUES (ST_MULTI(ST_BuildArea(ST_Force2d(ST_GeomFromText('{feat.geom}',31259)))), '{dxf_trak}-{dxf_layer_name}', '{dxf_text}', {floor_int});"
            #         # print("my insert is: ", sql_insert)
            #         cur.execute(sql_insert)
            #         conn.commit()

            # if dxf_layer_name in cad_label_layers:
            #     label_geom_types = ['MultiPoint', 'Point', 'Point25D', 'LineString25D', 'LineString']
            #     linestring_labels = ['LineString25D', 'LineString']

            #     if feat.geom.geom_type in label_geom_types:
            #         if dxf_text:
            #             if feat.geom.geom_type in linestring_labels:
            #  long_name, floor_num) VALUES (ST_MULTI(ST_Force2d(ST_StartPoint(ST_GeomFromText('{feat.geom}',31259)))), '{dxf_trak}-{dxf_layer_name}', '{dxf_text}', {floor_int});"
            #             elif feat.geom.geom_type == 'Polygon':
            #                 sql_insert = f"INSERT INTO geodata.{labels_table_name} (geom, short_name, long_name, floor_num) VALUES (ST_MULTI(ST_Force2d(ST_PointOnSurface(ST_GeomFromText('{feat.geom}',31259)))), '{dxf_trak}-{dxf_layer_name}', '{dxf_text}', {floor_int});"
            #             else:
            #                 sql_insert = f"INSERT INTO geodata.{labels_table_name} (geom, short_name, long_name, floor_num) VALUES (ST_MULTI(ST_Force2d(ST_GeomFromText('{feat.geom}',31259))), '{dxf_trak}-{dxf_layer_name}', '{dxf_text}', {floor_int});"
            #             cur.execute(sql_insert)
            #             conn.commit()

            #print(feat.fid, feat.geom.geom_type, feat.geom, feat.fields, feat.layer_name)
        #0 LINESTRING (7540750437 340250.600061613,752337.50231658 340250.678862686) ['Layer', 'SubClasses', 'ExtendedEntity', 'Linetype', 'EntityHandle', 'Text'] entities
    print("myset of types is : ", myset)
    cur.close()
    conn.close()
            
            

# import_dxf_files()



spaces_map = {'layer': 'Z_009', 'geom-type': 'polygon'}

# doors, tables, chairs, ramps, stairs  all as linestrings or multilinestrings
features = ['door', 'table', 'chair', 'ramp', 'stairs', 'inner-wall', 'outer-wall', 'window']
door_map = [{'layer': 'A2-TUER-SYM050', 'type': 'door'}, {'layer':'O_T49', 'type': 'door'}]

walls_map = [{'layer': 'M_A29', 'type':'outer-wall'}]

stairs = [{'layer': 'S_29', 'type': 'arrow or ramp'}, {'layer':'S_27', 'type':'stair'}]

windows = [{'layer': 'O_F49', 'type': 'window'}, {'layer': 'M_V29 (Fassadenverkleidung)', 'type': 'window'}]

raumstempl = [{'layer': 'GUT_RAUMSTEMPEL'}]

# sink = [{'layer': 'E_S29', 'type': 'sink'},]

dest_tables = ['building', 'buildingfloor', 'buildingfloorplanline', 'buildingfloorspace', ]



buildingfloor = ['outer-wall', 'window']

def create_building_floor():
    """
    This is the single polygon outlining the entire floor
    Generated by creating a polygon of the outerwalls linestrings
    """

    buildingfloor = ['outer-wall', 'window']
    


