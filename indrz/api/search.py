# search anything on campus
import json
import logging


from django.contrib.gis.gdal import OGRGeometry
from django.db.models import Q
from django.utils.translation import ugettext as _

from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from geojson import Feature, FeatureCollection

from poi_manager.models import Poi
from buildings.models import BuildingFloorSpace

logr = logging.getLogger(__name__)


def repNoneWithEmpty(string):
    if string is None:
        return ''
    else:
        return str(string)


@api_view(['GET'])
# @authentication_classes(TokenAuthentication)
@permission_classes((IsAuthenticated, ))
def search_any(request, q, format=None):
    permission_classes = (permissions.IsAuthenticated, )

    lang_code = "en"
    searchString = q

    poi_data = searchPoi(lang_code, searchString, "search")
    spaces_data = searchSpaces(lang_code, searchString, "search")

    if poi_data:
        return Response(poi_data, status=status.HTTP_200_OK)

    if spaces_data:
        return Response(spaces_data, status=status.HTTP_200_OK)

    else:
        return Response({"error": "no data found in local or api search"}, status=status.HTTP_404_NOT_FOUND)

    # =================================================================================================================================
    # external data api lookup finished, if entries present --> return them, else do a lookup in our local data.

def searchSpaces(lang_code, search_text, mode):
    """

    :param lang_code: such as "en" or "de"
    :param search_text: string value used to search agains
    :param mode: "autocomplete" or "search"
    :return:
    """

    if len(search_text) < 3:
        return None

    space_in = search_text.replace(" ", "")  # enable HS 04 H34   to return HS04H34
    spaces_data = BuildingFloorSpace.objects.filter(room_code__icontains=space_in)

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
                      "src": "indrz spaces room_code", "poi_id": ""}

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
        res_api = None

        if res_api:
            all_api_results = []
            if res_api.organizations:
                all_api_results.extend(res_api.organizations)
            if res_api.staff:
                all_api_results.extend(res_api.staff)
            if all_api_results:
                return Response(all_api_results)
        else:

            poi_results = searchPoi(lang_code, search_text, "autocomplete")
            spaces_data = searchSpaces(lang_code, search_text, 'autocomplete')

            if poi_results:
                return Response(poi_results, status=status.HTTP_200_OK)
            if spaces_data:
                return Response(spaces_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "sorry nothing found"}, status=status.HTTP_404_NOT_FOUND)
