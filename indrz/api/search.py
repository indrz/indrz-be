# search anything on campus
import logging
import re
from collections import OrderedDict
from itertools import chain

from django.db.models import Q
from django.utils.translation import get_language_from_request
from geojson import FeatureCollection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from buildings.models import BuildingFloorSpace
from buildings.serializers import BuildingFloorSpaceSerializer

logr = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def search_any(request, q, format=None):
    permission_classes = (permissions.IsAuthenticated, )

    if len(q) < 4:
        return Response({"error":"search length minimum 3 characters", "reason":"Sorry please enter 3 or more characters"}, status=status.HTTP_200_OK)

    if not q:
        return Response({"error":"empty search query", "reason":"Sorry search query values is null"}, status=status.HTTP_200_OK)

    lang_code = get_language_from_request(request)

    searchString = q

    # TODO uncomment to enable search people via TU api
    res_tu_api_response = tu_data(q, lang_code)
    poi_data = search_poi(lang_code, searchString)
    spaces_data = search_spaces(lang_code, searchString)

    # TODO remove custom db search was used for quick project start
    # spaces_custom_data = custom_db_query_tu(lang_code, searchString)
    campus_data = search_campus(searchString)
    building_data = search_buildings(searchString)
    bookway_data = search_for_shelf(searchString)
    gender_neutral_data = tu_gender_neutral_search(searchString)


    if bookway_data:
        bookway_data = bookway_data['features']

    if spaces_data:
        spaces_data = spaces_data['features']

    if poi_data:
        poi_data = poi_data['features']

    if campus_data:
        campus_data = campus_data['features']

    if building_data:
        building_data = building_data['features']

    if res_tu_api_response:
        res_tu_api_response = res_tu_api_response['features']

    if gender_neutral_data:
        gender_neutral_data = gender_neutral_data['features']

    all_results = chain(spaces_data, campus_data, poi_data, building_data, bookway_data,
                        res_tu_api_response, gender_neutral_data)

    return Response(FeatureCollection(all_results), status=status.HTTP_200_OK)

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    # ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
    #     and grouping quoted words together.
    #     Example:
    #
    #     >>> normalize_query('  some random  words "with   quotes  " and   spaces')
    #     ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    #
    # '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search_poi(lang_code, search_text):
    if lang_code == "de":
        pois = Poi.objects.filter(
            Q(name_de__icontains=search_text) |
            Q(name__icontains=search_text) |
            Q(poi_tags__icontains=search_text) |
            Q(category__cat_name_de__icontains=search_text)
        ).filter(enabled=True).prefetch_related('poiimages_set')
    else:
        pois = Poi.objects.filter(
            Q(name__icontains=search_text) |
            Q(poi_tags__icontains=search_text) |
            Q(category__cat_name__icontains=search_text)
        ).filter(enabled=True).prefetch_related('poiimages_set')

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

    campuses = Campus.objects.filter(Q(campus_name__icontains=search_text)  )

    if campuses:
        serializer = CampusSearchSerializer(campuses, many=True)
        return serializer.data
    else:
        return OrderedDict()

@api_view(['GET'])
def search_indrz(request, campus_id, search_string, format=None):
    # query_string = ''
    # found_entries = None

    # if using a url like http://www.campus.com/search/?q=sometext
    # use this if statement and indent code block

    # if ('q' in request.GET) and request.GET['q'].strip():
    #     query_string = request.GET['q']

    entry_query = get_query(search_string, ['short_name', 'long_name', 'room_code', 'room_description'])

    # return only first 20 results
    found_entries = BuildingFloorSpace.objects.filter(fk_building__fk_campus=campus_id).filter(entry_query)[:20]

    # buildings_on_campus = BuildingFloorSpace.objects.filter(Q(short_name__icontains=search_string) | Q(room_code__icontains=search_string))
    serializer = BuildingFloorSpaceSerializer(found_entries, many=True)

    if found_entries:

        return Response(serializer.data)

    # elif:
    #     pass
        # return Response({'error': 'sorry nothing found with the text:  ' + search_string})

    else:
        return Response({'error': 'sorry nothing found with the text:  ' + search_string})

# old silly search
# @api_view(['GET'])
# def campus_search(request, campus_id, search_string, format=None):
#     """
#     Search campus spaces in system and pois
#     """
#     if request.method == 'GET':
#
#         buildings_on_campus = BuildingFloorSpace.objects.filter(Q(short_name__icontains=search_string) | Q(room_code__icontains=search_string))
#         serializer = BuildingFloorSpaceSerializer(buildings_on_campus, many=True)
#
#         return Response(serializer.data)

