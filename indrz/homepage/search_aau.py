# search anything on campus
import collections
import json
import re
import ast
import logging
from collections import OrderedDict

from django.contrib.gis.db.models.functions import AsGeoJSON
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from mptt.templatetags.mptt_tags import cache_tree_children
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import APIException
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from buildings.models import BuildingFloorSpace
from buildings.serializers import BuildingFloorSpaceSerializer
from homepage import bach_calls

# from django.http import Http404, HttpResponse, HttpResponseServerError
# from django.db.utils import DatabaseError
# from django.core.exceptions import PermissionDenied
# from models import Language
# import re
# from log_routes import log_request
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import ugettext as _
from django.core.serializers import serialize
from geojson import Feature, FeatureCollection
from django.db import connection

from poi_manager.models import Poi, PoiCategory
from poi_manager.serializers import PoiSerializer, PoiSimpleSerializer

from homepage.aau_campus_api import AAICampusAPI, aau_api_res_source

logr = logging.getLogger(__name__)


# search for what is close to a given coordinate and return a list
# of strings and coordinates - coordinates must contain Lon, Lat and Layer

# @jsonrpc_method('searchCoordinates(q=dict) -> dict', validate=True)
@api_view(['GET'])
def search_coordinates(request, q, format=None):
    if q.keys().index('coordinates') < 0:
        raise Exception("Couldn't find coordinates in Parameter q")
    coordinates = q['coordinates']
    lon = float(coordinates['lon'])
    lat = float(coordinates['lat'])
    layer = int(coordinates['layer'])

    distance_bound = 5  # 5 meters

    # build geom string - this should be safe from any sql injection as lon and lat are both floats
    geom = "ST_SetSrid(ST_GeomFromText('POINT(" + str(lon) + " " + str(lat) + ")'),900913)"

    sql = "SELECT search_string, text_type, external_id, st_asgeojson(geom) as geom, \
        st_asgeojson(st_PointOnSurface(geom)) as center, \
        ST_Distance( geom," + geom + ") as dist, layer, external_ref_name, aks_nummer, building \
        FROM geodata.search_index_v \
        WHERE layer=%(layer)s \
            AND ST_Distance( geom," + geom + " ) < %(distance_bound)s \
        ORDER BY priority DESC, ST_Distance(geom," + geom + ") ASC LIMIT 30"

    rows = []



    cursor = connection.cursor()

    cursor.execute(sql,
                   {"layer": layer, "distance_bound": distance_bound})
    db_rows = cursor.fetchall()

    for row in db_rows:
        external_ref_name = row[7]
        # query to bach api
        external_data = bach_calls.bach_get_room_by_pk_big(external_ref_name)

        name_de = name_en = row[0]
        if external_data is not None and 'roomcode' in external_data:  # old value was 'roomname' now roomcode
            name_de = name_en = external_data['roomcode']
            # end if

        obj = {"name_de": name_de, "name_en": name_en, "type": row[1], "external_id": row[2], "geometry": row[3],
               "centerGeometry": row[4], "dist": row[5], "layer": int(row[6]), "aks_nummer": row[8], "building": row[9],
               "externalRefName": external_ref_name,
               "externalData": external_data,
               }
        new_feature = Feature(geometry=row[3], properties=obj)
        rows.append(new_feature)

    searchString = str(lon) + "," + str(lat) + "," + str(layer)

    retVal = {"searchString": searchString, "searchResult": rows, "length": len(db_rows)}

    return Response(retVal)


# search for what is close to a given coordinate and return a list of strings and coordinates
# - coordinates must contain Lon, Lat and Layer
# @jsonrpc_method('searchCoordinatesPOI(q=dict) -> dict', validate=True)

@api_view(['GET'])
def search_coordinates_on_poi(request, q, format=None):
    if q.keys().index('coordinates') < 0:
        raise Exception("Couldn't find coordinates in Parameter q")
    coordinates = q['coordinates']
    lon = float(coordinates['lon'])
    lat = float(coordinates['lat'])
    layer = int(coordinates['layer'])

    distance_bound = 1  # 5 meters

    # build geom string - this should be safe from any sql injection as lon and lat are both floats
    geom = "ST_SetSrid(ST_GeomFromText('POINT(" + str(lon) + " " + str(lat) + ")'),900913)"

    sql = "SELECT search_string, text_type, external_id, ST_asgeojson(geom) as geom, \
    ST_asgeojson(ST_PointOnSurface(geom)) as center, \
    ST_Distance(geom," + geom + ") as dist, layer, external_ref_name, aks_nummer, building \
    FROM geodata.search_index_v \
    WHERE text_type='poi' \
    AND layer=%(layer)s \
    AND ST_Distance(geom," + geom + ") < %(distance_bound)s \
    ORDER BY priority DESC, ST_Distance(geom," + geom + ") \
    ASC LIMIT 30"

    rows = []

    from django.db import connection

    cursor = connection.cursor()
    cursor.execute(sql,
                   {"layer": layer, "distance_bound": distance_bound})
    dbRows = cursor.fetchall()
    for row in dbRows:
        external_ref_name = row[7]
        # query to bach api
        external_data = bach_calls.bach_get_room_by_pk_big(external_ref_name)
        obj = {"name_de": row[0], "name_en": row[0], "type": row[1], "external_id": row[2], "geometry": row[3],
               "centerGeometry": row[4], "dist": row[5], "layer": int(row[6]), "aks_nummer": row[8], "building": row[9],
               "externalRefName": external_ref_name,
               "externalData": external_data,
               }
        rows.append(obj)

    searchString = str(lon) + "," + str(lat) + "," + str(layer)

    retVal = {"searchString": searchString, "searchResult": rows, "length": len(dbRows)}

    return Response(retVal)


def repNoneWithEmpty(string):
    if string is None:
        return ''
    else:
        return str(string)


# returns the entrance which is nearest to this room+
@api_view(['GET'])
def getAssignedEntrance(request, aks, layer, format=None):
    """
    input aks as string
    input layer as integer

    output dictionary of entrance-id,
         entrance-name-de, entrance-name-en,
         entrance-lat, entrance-lon
    """
    from django.db import connection

    cursor = connection.cursor()

    sql = "SELECT entrance_poi_id FROM geodata."

    if (layer == -1 or layer == "-1"):
        sql += "ug01"
    elif (layer == 0 or layer == "0"):
        sql += "eg00"
    elif (layer > 0):
        sql += "og0" + str(layer)

    sql += "_rooms where aks_nummer = %(aks)s"
    cursor.execute(sql, {"aks": aks})
    results = cursor.fetchall()

    if len(results) > 0:
        entranceID = results[0][0]

        cursor.execute(
            "SELECT description, description_en, ST_asgeojson(geom) AS geojson_geom FROM geodata.poi_list WHERE id=%(id)s",
            {"id": entranceID})
        res = cursor.fetchall()

        if cursor.rowcount > 0:
            entrance_point = json.loads(res[0][2])
            entrance_lat = entrance_point["coordinates"][1]
            entrance_lon = entrance_point["coordinates"][0]

        if len(res) > 0:
            valid_resp = {"id": repNoneWithEmpty(entranceID), "de": repNoneWithEmpty(res[0][0]),
                    "en": repNoneWithEmpty(res[0][1]),
                    "entrance_lat": entrance_lat,
                    "entrance_lon": entrance_lon}

            return Response(valid_resp)
    # if nothing found
    invalid_return = {"id": "", "de": "", "en": "", "entrance_lat": "", "entrance_lon": ""}
    return Response(invalid_return)


    # search for strings and return a list of strings and coordinates


def has_front_office(orgid):
    """

    :param data:
    :return:
    """

    from django.db import connection
    cursor = connection.cursor()

    if orgid != None and orgid != "":
        organization_details = bach_calls.bach_get_organization_details(orgid)
        if organization_details != None and len(organization_details) > 0:
            org_info = {"location": organization_details["location"],
                        "name": organization_details["label"],
                        "geom": None}

            query_geo = """SELECT  layer as floor, st_asgeojson(st_PointOnSurface(geom)) AS center
              FROM geodata.search_index_v
              WHERE external_id = \'{0}\'""".format(organization_details["location"])

            cursor.execute(query_geo)
            geos = cursor.fetchone()

            foo = ast.literal_eval(geos[1])
            floor_level = (geos[0])

            org_info.update({'geom': foo, 'floor_num': floor_level})

            return org_info
    else:
        return None

def setNameLabel(somethin):
    # bach_key_priority = {"roomname_de":1, "label":2, "fancyname_de":3, "category_de": 4}

    name_key = None

    if "roomname_de" in somethin:
        name_key = somethin['roomname_de']
    elif "label" in somethin:
        name_key = somethin['label']
    elif "fancyname_de" in somethin:
        name_key = somethin['fancyname_de']
    elif "category_de" in somethin:
        name_key = somethin['category_de']
    elif "roomcode" in somethin:
        name_key = somethin['roomcode']
    else:
        name_key = None

    return name_key

from rest_framework import permissions

@api_view(['GET'])
# @authentication_classes(TokenAuthentication)
@permission_classes((IsAuthenticated, ))
def search_any(request, q, format=None):
    permission_classes = (permissions.IsAuthenticated, )

    lang_code = request.LANGUAGE_CODE
    searchString = q

    res_aau_api = AAICampusAPI().search(q)

    # print("res_aau_api ", res_aau_api)
    # res_aau_api = False

    if res_aau_api:

        src = aau_api_res_source(res_aau_api)

        if src == 'staff':
            f = res_aau_api.staff

        elif src == 'rooms':
            f = res_aau_api.rooms

        elif src == 'organizations':
            f = res_aau_api.organizations

        else:
            f = [{"error": "nothing found with: " + q, "cat": src}]

        roomcodes = [val['roomcode'] for val in f]
        spaces = BuildingFloorSpace.objects.filter(room_code__in=roomcodes)
        features = []

        for space in spaces:

            geom = json.loads(space.multi_poly.geojson)

            name = ""

            props = dict()

            for code in f:
                if code['roomcode'] == space.room_code:
                    props.update(code)

            space_center_geom = json.loads(space.centerGeometry.geojson)
            props.update({"spaceid": space.pk, "building": space.fk_building.building_name,
                          "floor_num": str(space.floor_num), "centerGeometry": space_center_geom})

            feature = Feature(geometry=geom, properties=props)
            features.append(feature)

        fc = FeatureCollection(features)

        if spaces:
            return Response(fc)
        else:
            return Response({"error": "no geometry found for that query: " + q}, status=status.HTTP_404_NOT_FOUND)


    # =================================================================================================================================
    # external data api lookup finished, if entries present --> return them, else do a lookup in our local data.
    else:
        poi_data = searchPoi(lang_code, searchString, "search")
        spaces_data = searchSpaces(lang_code, searchString, "search")

        if poi_data:
            return Response(poi_data, status=status.HTTP_200_OK)
        elif spaces_data:
            return Response(spaces_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "no data found in localdb"}, status=status.HTTP_404_NOT_FOUND)


def searchSpaces(lang_code, search_text, mode):

    spaces_data = BuildingFloorSpace.objects.filter(Q(room_code__icontains=search_text)
                                                    | Q(room_description__icontains=search_text))

    if spaces_data:

        s_features = []
        ac_data = []
        for sd in spaces_data:

            s_data = {"label": sd.room_code, "name": sd.room_code, "name_de": sd.room_code, "type": "space",
                      "external_id": sd.room_external_id,
                      "centerGeometry": json.loads(sd.multi_poly.centroid.geojson),
                      "floor_num": sd.floor_num,
                      "building": sd.fk_building.name,
                      "roomcode": sd.room_code,
                      "parent": "",
                      "fk_poi_category": {'id': "", 'cat_name': ""},
                      "icon": "",
                      "src": "indrz spaces", "poi_id": ""}

            s_feature = Feature(geometry=json.loads(sd.multi_poly.geojson), properties=s_data)
            ac_data.append(s_data)
            s_features.append(s_feature)
        fc = FeatureCollection(s_features)

        if mode == 'search':
            return fc
        if mode == 'autocomplete':
            return ac_data
    else:
        return None


def searchPoi(lang_code, search_text, mode):

    poi_list = []

    pois = Poi.objects.filter(Q(name__icontains=search_text) | Q(poi_tags__icontains=search_text)
                              | Q(fk_poi_category__cat_name__icontains=search_text)).filter(enabled=True)

    if lang_code == "de":
        pois = Poi.objects.filter(Q(name_de__icontains=search_text) | Q(poi_tags__icontains=search_text)
                                  | Q(fk_poi_category__cat_name_de__icontains=search_text)).filter(enabled=True)

    build_name = ""
    icon_path = ""

    for poi in pois:
        if hasattr(poi.fk_building, 'building_name'):
            build_name = poi.fk_building.building_name
        if hasattr(poi.fk_poi_category.fk_poi_icon, 'poi_icon'):
            icon_path = str(poi.fk_poi_category.fk_poi_icon.poi_icon)

        center_geom = json.loads(poi.geom.geojson)

        if lang_code == "de":
            poi_data = {"label": poi.name_de, "name": poi.name_de, "name_de": poi.name_de, "type": "", "external_id": "",
                     "centerGeometry": center_geom,
                     "floor_num": poi.floor_num,
                     "building": build_name, "aks_nummer": "",
                     "roomcode": "",
                     "parent": poi.fk_poi_category.cat_name_de,
                        "fk_poi_category": {'id': poi.fk_poi_category_id, 'cat_name': poi.fk_poi_category.cat_name_de},
                    "icon": icon_path,
                        "poi_link_unique": "/?poi-id=" + str(poi.id) + "&floor=" + str(poi.floor_num),
                        "poi_link_category": "/?poi-cat-id=" + str(poi.fk_poi_category_id),
                     "src": "poi db", "poi_id": poi.id}

            if mode == "search":
                new_feature_geojson = Feature(geometry=center_geom, properties=poi_data)
                poi_list.append(new_feature_geojson)
            elif mode == "autocomplete":
                poi_list.append(poi_data)

        else:
            poi_data = {"label": poi.name, "name": poi.name, "name_de": poi.name_de, "type": "", "external_id": "",
                     "centerGeometry": center_geom,
                     "floor_num": poi.floor_num,
                     "building": build_name, "aks_nummer": "",
                     "roomcode": "",
                     "parent": poi.fk_poi_category.cat_name,
                     "fk_poi_category": {'id': poi.fk_poi_category_id, 'cat_name': poi.fk_poi_category.cat_name_en},
                        "poi_link_unique": "/?poi-id=" + str(poi.id) + "&floor=" + str(poi.floor_num),
                        "poi_link_category": "/?poi-cat-id=" + str(poi.fk_poi_category_id),
                     "icon": icon_path,
                     "src": "poi db", "poi_id": poi.id}

            if mode == "search":
                new_feature_geojson = Feature(geometry=center_geom, properties=poi_data)
                poi_list.append(new_feature_geojson)
            elif mode == "autocomplete":
                poi_list.append(poi_data)

    spaces_list = [{"name": _(space.room_code), "name_" + lang_code: _(space.room_code), "id": space.id} for
                   space in
                   BuildingFloorSpace.objects.filter(room_code__isnull=False).filter(room_code__icontains=search_text)]

    # local_data = poi_list + spaces_list
    if poi_list:

        final_geojs_res = FeatureCollection(features=poi_list)
    else:
        final_geojs_res = False

    if mode == "search":
        if final_geojs_res:
            return final_geojs_res
        else:
            return False
    else:
        if poi_list:
            return poi_list
        else:
            return False


class searchAutoComplete(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, search_text, format=None):

        lang_code = request.LANGUAGE_CODE

        res_aau_api = AAICampusAPI().search(search_text)


        if res_aau_api:
            for x in res_aau_api:
                if x:
                    return Response(x)

            # return Response(res_aau_api)
        else:
            # ===========================================================================
            # local Postgresql search_index_v data

            poi_results = searchPoi(lang_code, search_text, "autocomplete")
            spaces_data = searchSpaces(lang_code, search_text, 'autocomplete')

            if poi_results:
                return Response(poi_results, status=status.HTTP_200_OK)
            elif spaces_data:
                return Response(spaces_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "sorry nothing found"}, status=status.HTTP_404_NOT_FOUND)


class AauApi(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = (JSONParser,)

    def get(self, request, q, format=None):

        x = AAICampusAPI().search(q)
        return Response({'response': x, })

