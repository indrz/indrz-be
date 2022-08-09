# search anything on campus
import re
from collections import OrderedDict
from itertools import chain

from django.db.models import Q
from geojson import FeatureCollection
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from buildings.models import BuildingFloorSpace, Building, Campus
from buildings.serializers import BuildingSerializer, CampusSearchSerializer, BuildingFloorSpaceSerializer
from poi_manager.models import Poi
from poi_manager.serializers import PoiSerializer


def search_spaces(lang_code, search_text, mode):
    """
    :param lang_code: such as "en" or "de"
    :param search_text: string value used to search agains
    :param mode: "autocomplete" or "search"
    :return:
    """

    if len(search_text) < 3:
        return None

    space_in = search_text.replace(" ", "")  # enable HS 04 H34   to return HS04H34

    spaces_data = BuildingFloorSpace.objects.filter(Q(short_name__icontains=search_text) |
                                                    Q(room_code__icontains=space_in) | Q(
        room_description__icontains=search_text)
                                                    )

    if spaces_data:
        serializer = BuildingFloorSpaceSerializer(spaces_data, many=True)
        return serializer.data
    else:
        return OrderedDict()


def search_poi(lang_code, search_text):
    pois = Poi.objects.filter(Q(name__icontains=search_text) | Q(poi_tags__icontains=search_text)
                              | Q(category__cat_name__icontains=search_text)).filter(enabled=True)

    if lang_code == "de":
        pois = Poi.objects.filter(Q(name_de__icontains=search_text) | Q(poi_tags__icontains=search_text)
                                  | Q(category__cat_name_de__icontains=search_text)).filter(enabled=True)

    if pois:
        serializer = PoiSerializer(pois, many=True)
        return serializer.data
    else:
        return OrderedDict()


def search_buildings(search_text):
    buildings = Building.objects.filter(Q(building_name__icontains=search_text) | Q(street__icontains=search_text))

    if buildings:
        serializer = BuildingSerializer(buildings, many=True)
        return serializer.data
    else:
        return OrderedDict()


def search_campus(search_text):
    campuses = Campus.objects.filter(Q(campus_name__icontains=search_text))

    if campuses:
        serializer = CampusSearchSerializer(campuses, many=True)
        return serializer.data
    else:
        return OrderedDict()


@api_view(['GET'])
# @authentication_classes(TokenAuthentication)
@permission_classes((IsAuthenticated,))
def search_any(request, q, format=None):
    permission_classes = (permissions.IsAuthenticated,)

    lang_code = "en"
    searchString = q

    poi_data = search_poi(lang_code, searchString)
    spaces_data = search_spaces(lang_code, searchString, "search")
    campus_data = search_campus(searchString)
    building_data = search_buildings(searchString)

    if campus_data:
        campus_data = campus_data['features']
    if spaces_data:
        spaces_data = spaces_data['features']
    if poi_data:
        poi_data = poi_data['features']
    if building_data:
        building_data = building_data['features']

    all_results = chain(spaces_data, campus_data, poi_data, building_data)

    # return Response(ress, status=status.HTTP_200_OK)
    return Response(FeatureCollection(all_results), status=status.HTTP_200_OK)
