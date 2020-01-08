# search anything on campus
import json
import ast
import logging

from django.db.models import Q
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from buildings.models import BuildingFloorSpace
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import ugettext as _
from geojson import Feature, FeatureCollection
from django.db import connection

from django.contrib.gis.gdal import OGRGeometry

from poi_manager.models import Poi

from api.tu_campus_api import TuCampusAPI, api_res_source


logr = logging.getLogger(__name__)



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



from rest_framework import permissions

@api_view(['GET'])
# @authentication_classes(TokenAuthentication)
@permission_classes((IsAuthenticated, ))
def search_any(request, q, format=None):
    permission_classes = (permissions.IsAuthenticated, )

    lang_code = "en"
    searchString = q

    res_aau_api = TuCampusAPI().search(q)

    # print("res_aau_api ", res_aau_api)
    # res_aau_api = False

    if res_aau_api:

        src = api_res_source(res_aau_api)

        if src == 'staff':
            f = res_aau_api.staff

        # elif src == 'rooms':
        #     f = res_aau_api.rooms

        elif src == 'organizations':
            f = res_aau_api.organizations

        else:
            f = [{"error": "nothing found with: " + q, "cat": src}]



        all_api_results = []
        if res_aau_api.organizations:
            all_api_results.extend(res_aau_api.organizations)
        if res_aau_api.staff:
            all_api_results.extend(res_aau_api.staff)


        roomcodes = list(set(val['roomcode'] for val in all_api_results))
        print(roomcodes)

        spaces = BuildingFloorSpace.objects.filter(room_code__in=roomcodes)
        features = []

        for space in spaces:

            g = OGRGeometry(space.geom.wkt)

            geom = json.loads(g.geojson)

            name = ""

            props = dict()

            for code in f:
                if code['roomcode'] == space.room_code:
                    props.update(code)

            # space_center_geom = json.loads(space.centerGeometry.geojson)
            props.update({"space_id": space.pk, "building": space.fk_building_floor.fk_building.building_name,
                          "floor_num": str(space.floor_num), "floor_name":str(space.floor_name), "centerGeometry": "space_center_geom"})

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
        # poi_data = searchPoi(lang_code, searchString, "search")
        spaces_data = searchSpaces(lang_code, searchString, "search")

        # if poi_data:
        #     return Response(poi_data, status=status.HTTP_200_OK)
        if spaces_data:
            return Response(spaces_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "no data found in localdb"}, status=status.HTTP_404_NOT_FOUND)


def searchSpaces(lang_code, search_text, mode):

    # spaces_data = BuildingFloorSpace.objects.filter(Q(room_code__icontains=search_text)
    #                                                 | Q(room_description__icontains=search_text))

    spaces_data = BuildingFloorSpace.objects.filter(room_code__icontains=search_text)

    if spaces_data:

        s_features = []
        ac_data = []
        for sd in spaces_data:

            s_data = {"label": sd.room_code, "name": sd.room_code, "name_de": sd.room_code, "type": "space",
                      "external_id": sd.room_external_id,
                      "centerGeometry": json.loads(sd.geom.centroid.geojson),
                      "floor_num": sd.floor_num,
                      "floor_name": sd.floor_name,
                      "building": sd.fk_building_floor.fk_building.name,
                      "roomcode": sd.room_code,
                      "space_id": sd.id,
                      "parent": "",
                      "category": {'id': "", 'cat_name': ""},
                      "icon": "",
                      "src": "indrz spaces", "poi_id": ""}

            s_feature = Feature(geometry=json.loads(sd.geom.geojson), properties=s_data)
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
                              | Q(category__cat_name__icontains=search_text)).filter(enabled=True)

    if lang_code == "de":
        pois = Poi.objects.filter(Q(name_de__icontains=search_text) | Q(poi_tags__icontains=search_text)
                                  | Q(category__cat_name_de__icontains=search_text)).filter(enabled=True)

    build_name = ""
    icon_path = ""

    if pois:
        for poi in pois:
            if hasattr(poi.fk_building, 'building_name'):
                build_name = poi.fk_building.building_name
            if hasattr(poi.category.fk_poi_icon, 'poi_icon'):
                icon_path = str(poi.category.fk_poi_icon.poi_icon)

            center_geom = json.loads(poi.geom.geojson)

            if lang_code == "de":
                poi_data = {"label": poi.name_de, "name": poi.name_de, "name_de": poi.name_de, "type": "",
                            "external_id": "",
                            "centerGeometry": center_geom,
                            "floor_num": poi.floor_num,
                            "floor_name": poi.floor_name,
                            "building": build_name, "aks_nummer": "",
                            "roomcode": "",
                            "parent": poi.category.cat_name_de,
                            "category": {'id': poi.category_id,
                                                'cat_name': poi.category.cat_name_de},
                            "icon": icon_path,
                            "poi_link_unique": "/?poi-id=" + str(poi.id) + "&floor=" + str(poi.floor_num),
                            "poi_link_category": "/?poi-cat-id=" + str(poi.category_id),
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
                         "parent": poi.category.cat_name,
                         "category": {'id': poi.category_id, 'cat_name': poi.category.cat_name_en},
                            "poi_link_unique": "/?poi-id=" + str(poi.id) + "&floor=" + str(poi.floor_num),
                            "poi_link_category": "/?poi-cat-id=" + str(poi.category_id),
                         "icon": icon_path,
                         "src": "poi db", "poi_id": poi.id}

                if mode == "search":
                    new_feature_geojson = Feature(geometry=center_geom, properties=poi_data)
                    poi_list.append(new_feature_geojson)
                elif mode == "autocomplete":
                    poi_list.append(poi_data)

    spaces_list = [{"name": _(space.room_code), "name_" + lang_code: _(space.room_code), "id": space.id, "space_id": space.id} for
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

        lang_code = "en"

        res_api = TuCampusAPI().search(search_text)

        print("in AUTOCOMPLETE ", res_api)


        if res_api:
            all_api_results = []
            if res_api.organizations:
                all_api_results.extend(res_api.organizations)
            if res_api.staff:
                all_api_results.extend(res_api.staff)



            if all_api_results:
                return Response(all_api_results)
            # for x in res_api:
            #     if x:
            #         return Response(x)

            # return Response(res_aau_api)
        else:
            # ===========================================================================
            # local Postgresql search_index_v data

            # poi_results = searchPoi(lang_code, search_text, "autocomplete")
            spaces_data = searchSpaces(lang_code, search_text, 'autocomplete')

            # if poi_results:
            #     return Response(poi_results, status=status.HTTP_200_OK)
            if spaces_data:
                return Response(spaces_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "sorry nothing found"}, status=status.HTTP_404_NOT_FOUND)


class TuApi(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = (JSONParser,)

    def get(self, request, q, format=None):

        x = TuCampusAPI().search(q)
        return Response({'response': x, })

