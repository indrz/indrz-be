# search anything on campus
import json
import logging

from django.db.models import Q
from geojson import Feature, FeatureCollection
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from buildings.models import BuildingFloorSpace
from poi_manager.models import Poi
from poi_manager.serializers import PoiSerializer

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

    poi_data = searchPoi(lang_code, searchString)
    spaces_data = searchSpaces(lang_code, searchString, "search")

    if poi_data:
        return Response(poi_data, status=status.HTTP_200_OK)

    if spaces_data:
        return Response(spaces_data, status=status.HTTP_200_OK)

    else:
        return Response({"error": "no data found in local or api search"}, status=status.HTTP_404_NOT_FOUND)

    # =================================================================================================================================
    # external data api lookup finished, if entries present --> return them, else do a lookup in our local data.
def search_only(q, lang_code):

    # force 4 or more characters for search functions
    if len(q) < 3:
        return Response({"error":"4 or more characters needed for search"}, status=status.HTTP_200_OK)

    searchString = q

    # match a coodinate pair with floor num separated by ,  ex) 123.123,564.456,4
    if re.match("[-]?\d+\.?\d+,\d+\.\d+,\d+$", searchString):
        is_xyz = True

    # search external unique ids
    # find BIG unique code
    if re.match("([0-9]{0,3}_[0-9]{0,2}_)([a-zA-Z]{0,2}[0-9]{0,2}_[0-9]{0,8})?", searchString.upper()):
        # 001_10  is the first part needed
        # 001_10_OG01_1902721  after 6th char is optional

        spaces_aks = searchSpaces(searchString, "search")

        if spaces_aks:
            return spaces_aks
        else:
            return {"error":"no data found"}


def searchSpaces( search_text, mode):
    """
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


def searchPoi(lang_code, search_text):

    pois = Poi.objects.filter(Q(name__icontains=search_text) | Q(poi_tags__icontains=search_text)
                              | Q(category__cat_name__icontains=search_text)).filter(enabled=True)

    if lang_code == "de":
        pois = Poi.objects.filter(Q(name_de__icontains=search_text) | Q(poi_tags__icontains=search_text)
                                  | Q(category__cat_name_de__icontains=search_text)).filter(enabled=True)

    if pois:
        serializer = PoiSerializer(pois, many=True)
        return serializer.data
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

            poi_results = searchPoi(lang_code, search_text)
            spaces_data = searchSpaces(lang_code, search_text, 'autocomplete')

            if poi_results:
                return Response(poi_results, status=status.HTTP_200_OK)
            if spaces_data:
                return Response(spaces_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "sorry nothing found"}, status=status.HTTP_404_NOT_FOUND)
