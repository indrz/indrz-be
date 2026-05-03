import collections
import json
import logging
import re

from django.db import connection
from geojson import Feature, FeatureCollection
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from bookway.models import ShelfData, BookShelf
from bookway.serializers import ShelfdataSerializer, BookshelfSerializer

logr = logging.getLogger(__name__)


def create_geojson(data, key_value, shelfpoly=False):
    if not data:
        return None

    d = collections.OrderedDict()

    d["id"] = data[5]
    d["shelfID"] = data[0]
    d["shelfSide"] = data[0]
    d['shelf-side'] = data[1]
    shelfid = data[0]
    floor = data[3]
    building_floor_id = data[4]

    d["m-from"] = 0
    d["m-to"] = 1
    d["mFrom"] = 0
    d["mTo"] = 1
    d["location"] = (d["m-to"] + d["m-from"]) / 2
    d["name"] = key_value
    d["building"] = "LC"
    d["src"] = "indrz bookway"
    d["src_icon"] = "book"
    d["icon"] = "/poi_icons/autocomplete_bookway.png"
    d["floor"] = data[3]
    d["floor_num"] = float(data[3])

    offset_value = 1

    if d['shelf-side'] == 'R':
        offset_value = -1

    sql_shelf_geom = """
        SELECT
            ST_ASGeojson(ST_LineInterpolatepoint(ST_OffsetCurve((ST_Dump(bs.geom)).geom, {offset_value}),0.2)) as geom,
ST_ASGeojson(ST_Buffer(bs.geom, (0.25)::double precision, 'endcap=flat'::text)) AS geom_poly,
            bf.floor_num as floor_num,
            '{shelfid}' as shelf_id, bf.floor_name

        FROM
            library.bookshelf AS bs
        JOIN django.buildings_buildingfloor AS bf ON (bf.id = bs.floor_id)
        WHERE id_letter = '{shelfid}' 
            AND bs.floor_id = {building_floor_id}
        """.format(building_floor_id=building_floor_id, shelfid=shelfid, offset_value=offset_value)

    cursor = connection.cursor()
    cursor.execute(sql_shelf_geom)

    shelf_res_geo = cursor.fetchone()

    if shelf_res_geo:

        d['floor_num'] = shelf_res_geo[2]
        d['floor_name'] = shelf_res_geo[4]
        # d['measure'] = shelf_res_geo[2]
        d['key'] = key_value

        n_feature = Feature(geometry=json.loads(shelf_res_geo[0]), properties=d)

        if shelfpoly:
            n_feature = Feature(geometry=json.loads(shelf_res_geo[1]), properties=d)

        return n_feature
    else:
        return None


def _convert(val):
    try:
        float(val)
        return val
    except ValueError:
        return '"%s"' % val


def search_for_shelf(key_value):
    ky_array = re.split(r"[^\d\w]+", key_value.upper())

    where_clause = "{%s}" % ",".join(_convert(i) for i in ky_array)

    sql_base = """
        SELECT
          sd.external_id, -- 0
          sd.side,
          django.commonness('{where_clause}', sys_from_array) + django.commonness('{where_clause}', sys_to_array) AS commonness, -- 3
          sd.floor, -- 4,
          sd.building_floor_id,
          sd.id
        FROM
          django.bookway_shelfdata AS sd

        WHERE
          '{where_clause}' BETWEEN django.equalize_arrays('{where_clause}', sys_from_array, '0') 
                AND django.equalize_arrays('{where_clause}', sys_to_array, 'Z')
                AND django.commonness('{where_clause}', sys_from_array) + django.commonness('{where_clause}', sys_to_array) > 0
        ORDER BY
          commonness DESC
        LIMIT 20
    """.format(where_clause=where_clause)

    shelf_res = None
    try:
        cursor = connection.cursor()
        cursor.execute(sql_base)
        shelf_res = cursor.fetchone()
    except Exception as e:
        logr.error(f"An error occurred in search_for_shelf: {e}")

    if shelf_res:
        return shelf_res
    else:
        sql_opt2 = """
            SELECT
              sd.external_id, -- 0
              sd.side,
              django.commonness('{where_clause}', sys_from_array) + django.commonness('{where_clause}', sys_to_array) AS commonness, -- 3
              sd.floor, -- 4,
              sd.building_floor_id,
              sd.id
            FROM
              django.bookway_shelfdata AS sd

            WHERE
                django.commonness('{where_clause}', sys_from_array) + django.commonness('{where_clause}', sys_to_array) > 0
                OR
                  '{where_clause}' BETWEEN django.equalize_arrays('{where_clause}', sys_from_array, '0') 
                    AND django.equalize_arrays('{where_clause}', sys_to_array, 'Z')
           
            ORDER BY
              commonness DESC
            LIMIT 1
        """.format(where_clause=where_clause)

        shelf_res2 = None
        try:
            cursor = connection.cursor()
            cursor.execute(sql_opt2)
            shelf_res2 = cursor.fetchone()
        except Exception as e:
            logr.error(f"An error occurred in search_for_shelf: {e}")

        if shelf_res2:
            return shelf_res2
        else:
            return None


def match_system(key_value):
    """
    get:
    Return a GeoJSON representation of a shelf

    :param request:
    :param key_value:
    :return:
    """
    result = search_for_shelf(key_value)

    if result:
        return Response(result)
    else:

        d = collections.OrderedDict()
        d["error"] = "nomatch"
        d["data-in"] = key_value
        d["num results"] = 0
        return Response(d)


class ShelfdataViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = ShelfData.objects.all()
    serializer_class = ShelfdataSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['external_id', 'system_from', 'system_to']


class BookshelfViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = BookShelf.objects.all()
    serializer_class = BookshelfSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['external_id', 'left_from_label', 'right_from_label']


    @action(detail=True)
    def shelfdata(self, request, *args, **kwargs):
        instance = self.get_object()
        sd = ShelfData.objects.filter(bookshelf=instance)
        serializer = ShelfdataSerializer(sd, many=True)
        return Response(serializer.data)


def rvk_call(rvk_id, location=False, shelfgeom=False, format=None):
    """
    if a space was used in the url it is encoded as %20
    :param request:
    :param q:
    :return:
    """
    # rvk_key = q.replace('%20', '_')
    # rvk_key = rvk_id['key'].replace('%20', '_')
    # rvk_key = rvk_id.replace('%20', '_')

    rvk_key = rvk_id.upper()

    if re.match(
            r"[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}([\.\-](([0-9]{1,5})|([A-Za-z]([0-9]{1,5})?)))?[ _]*[a-zA-Z][0-9]{1,3}.*",
            rvk_key):
        # query fo08r searching the shelf, this first part remains the same all the time
        sql = 'SELECT * FROM library.shelf_data WHERE main_cat = %(cat_main)s  AND sub_cat = %(cat_sub)s AND numbers <= CAST(%(numbers)s AS INT)'

        # regex saves named parameters (eg. ?P<cat_main>) in the regDict. you can access it with regDict["cat_main"]
        regex = r"(?P<cat_main>[a-zA-Z])"  # cat_main
        regex += r"(?:(?P<cat_sub>[a-zA-Z]))?"  # optional cat_sub
        regex += r"[ _]*(?P<numbers>[0-9]{3,5})"  # numbers
        regex += r"((?P<postNumbers>[-\.][0-9]{1,5})|(?P<postChar>[\.\-][A-Za-z])|((?P<postCharNumbers_Char>[\.\-][A-Za-z])(?P<postCharNumbers_Number>[0-9]{1,6})))?"
        regex += r"[ _]*(?P<author>[a-zA-Z][ _]*[0-9]{1,3}).*"  # author and rest

        # match the regex and save the named parameters in regDict (Dictionary)
        regexList = re.match(regex, rvk_key)
        regDict = regexList.groupdict()

        # ========================================================================================
        # CASES FOR SEARCH VALUE

        # normal
        if re.match(r"[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}[ _]+[a-zA-Z][ _]*[0-9]{1,3}.*", rvk_key):
            # ignore sections with numbers_2 or charnumber set (the thingies after the dot, or in the url after minus )
            sql += " and numbers_2 = 0 and charnumber_char is null and charnumber_digit = 0"

        # .numbers
        elif re.match(r"[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}([\.\-][0-9]{1,5})?[ _]+[a-zA-Z][ _]*[0-9]{1,3}.*", rvk_key):
            regDict["postNumbers"] = regDict["postNumbers"][1:]  # cut off first char which is the "-"
            sql += "and numbers_2 <= %(postNumbers)s and charnumber_char is null and charnumber_digit = 0"

        # .char
        elif re.match(r"[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}([\.\-][a-zA-Z])[ _]+[a-zA-Z][ _]*[0-9]{1,3}.*", rvk_key):
            regDict["postChar"] = regDict["postChar"][1:]  # cut off first char which is the "-"
            sql += " and numbers_2 = 0 and charnumber_char is not null and charnumber_char <= %(postChar)s and charnumber_digit = 0"

        # .char + numbers
        elif re.match(r"[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}([\.\-][a-zA-Z][0-9]{1,6})[ _]+[a-zA-Z][ _]*[0-9]{1,3}.*",
                      rvk_key):
            regDict["postCharNumbers_Char"] = regDict["postCharNumbers_Char"][1:]  # cut off first char which is the "-"
            sql += " and numbers_2 = 0 and charnumber_char is not null and charnumber_char <= %(postCharNumbers_Char)s and charnumber_digit <= cast(%(postCharNumbers_Number)s as int)"

        # CASES FOR SEARCH VALUE END
        # ========================================================================================

        # add author search
        sql += ' order by numbers desc, numbers_2 desc, charnumber_char desc, charnumber_digit desc, row_number desc;'
        # ========================================================================================
        # execute query

        from django.db import connection

        cursor = connection.cursor()

        if cursor is not None:
            cursor.execute(sql, regDict)

            # return HttpResponse(cursor.query)


            dbrow = cursor.fetchall()

            if (len(dbrow) > 0):
                # =======================================================================================
                # first find the right shelf (ignore author if result numbers < numbers, since it will contain everything; else search for shelf starting with author < request author)
                i = 0
                numbers = dbrow[0][5]
                author = dbrow[0][9]

                if int(numbers) == int(regDict["numbers"]):
                    while (author[:1] > regDict["author"][:1]) or (
                            author[:1] == regDict["author"][:1] and int(author[1:]) > int(regDict["author"][1:])):
                        i = i + 1
                        numbers = dbrow[i][5]
                        author = dbrow[i][9]

                shelfID = dbrow[i][10]
                shelfArea = dbrow[i][11]
                fachboden = dbrow[i][12]
                building = dbrow[i][15]
                floor = dbrow[i][14]

                # =======================================================================================
                # find out on which side of the shelf the section is. < 0.5: left, > 0.5: right
                # 1st get the number of sections
                sql = "SELECT shelf_area FROM library.shelfdata WHERE shelf_id = \'" + shelfID + "\' AND floor = \'" + floor + "\' GROUP BY shelf_area;"
                cursor.execute(sql)
                length = len(cursor.fetchall())

                # index of section divided through number of sections, minus 0,5 * length of section
                # (so we are in the middle of the section) and the whole thing *2 (in sql query), since we have 2 sides.
                # (ord(shelfArea) gives the ascii value of the character, eg a = 97, b = 98,...
                # (ord(shelfArea)-96 --> a = 1, b = 2, c = 3...
                # we do this to get the position of the shelf-area.
                sideIndicator = float((ord(shelfArea) - 96)) / float(length)
                sectionPosition = (float((ord(shelfArea) - 96)) / float(length) - 0.5 / float(length))

                # ========================================================================================

                # now get the geometry of the shelf
                # no sql injection possible since data comes from regex-view and is guaranteed to be in the right format.
                # sql = "select  ST_AsGeoJson(ST_Force_2d(geom)) from geodata.og0" + building[3:4] +
                # "_library_regal_lines where id_letter = \'" + shelfID + "\';"

                sql = "SELECT ST_AsGeoJson(ST_Line_Interpolate_Point" \
                      "(ST_OffsetCurve((SELECT geom FROM library.og0" + building[3:4] +\
                      "_library_regal_lines WHERE id_letter = \'" + shelfID + "\'),"

                if sideIndicator > 0.5:
                    sql += "-0.7), " + str(1 - (1 - sectionPosition) * 2) + "))"
                else:
                    sql += "0.7), " + str(sectionPosition * 2) + "))"

                cursor.execute(sql)
                dbrow = cursor.fetchall()
                if (len(dbrow) > 0):
                    geom = dbrow[0][0]
                    geomJson = json.loads(str(geom))

                    # get the highlighted geometry of the shelf
                    sql = "SELECT ST_AsGeoJson(geom) FROM library.og0" + building[3:4] +\
                          "_library_shelf_poly WHERE id_letter = \'" + shelfID + "\';"

                    cursor.execute(sql)
                    dbrow = cursor.fetchall()

                    shelfGeom = dbrow[0][0]
                    shelfGeomJson = json.loads(str(shelfGeom))
                    shelf_properties = {
                        "name": rvk_key,
                        "building": building[:2],
                        "floor_num": building[3:4],
                        "shelfID": shelfID,
                        "fachboden": fachboden,
                        "position": str(sectionPosition),
                    }
                    point_location = Feature(geometry=geomJson, properties=shelf_properties)
                    shelf_poly = Feature(geometry=shelfGeomJson, properties=shelf_properties)
                    result_collection = FeatureCollection([shelf_poly, point_location])

                    if location==True:
                        return point_location
                    elif shelfgeom==True:
                        return shelf_poly
                    else:
                        return result_collection

                else:
                    return Response({'error 4': 'len db row is 0'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error 3': 'no rvk found in first query'}, status=status.HTTP_404_NOT_FOUND)

        # execute query stuff end
        # ============================================================================================
        return Response({'error 2': 'query to DB returned nothing hmm'}, status=status.HTTP_404_NOT_FOUND)
    # return HttpResponse(returnVal)
    else:
        return Response({'error 1': 'boom the RVK code does not match sorry call us'}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# def book_location(request, rvk_id, format=None):
#
#     book_location_geojson = rvk_call(rvk_id, location=True)
#
#     return Response(book_location_geojson)
#
#
# @api_view(['GET'])
# def shelf_geom(request, rvk_id, format=None):
#
#     shelf_geometry = rvk_call(rvk_id, shelfgeom=True)
#
#     return Response(shelf_geometry)

@api_view(["GET", ])
def book_location(request, key_value):
    """
    get:
    Return a GeoJSON representation of a shelf

    :param request:
    :param key_value:
    :return:
    """
    result = search_for_shelf(key_value)

    if result:
        n_feature = create_geojson(result, key_value)
        if n_feature:
            return Response(n_feature)
    else:

        d = collections.OrderedDict()
        d["error"] = "nomatch"
        d["data-in"] = key_value
        d["num results"] = 0
        return Response(d)


@api_view(['GET'])
def shelf_poly(request, key_value, format=None):

    res = search_for_shelf(key_value)

    if res:
        g = create_geojson(res, key_value, shelfpoly=True)

        if g:
            return Response(g)
        else:
            return Response({"error":"could not create geojson"})
    else:
        return Response({"error":"could not find match for {key_value}".format(key_value=key_value)})

