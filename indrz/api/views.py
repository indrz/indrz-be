#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import traceback
import logging
from django.http import HttpResponse

from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.gis.db.models.functions import Centroid, AsGeoJSON

from buildings.models import BuildingFloorSpace

from geojson import Feature

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def autocomplete_list(request):
    '''-
    http://localhost:8000/api/v1/spaces/
    :param request: no parameters GET or POST
    :return: JSON Array of available search terms
    '''
    cur = connection.cursor()
    if request.method == 'GET' or request.method == 'POST':

        # searchString = request.GET.get('q','')

        # cur.execute("""SELECT search_string FROM geodata.search_index_v
        #                   WHERE replace(replace (upper(search_string), '.', ''),'.', '') LIKE upper(%(search_string)s)
        #                   GROUP BY search_string
        #                   ORDER BY length(search_string) LIMIT 100""",
        #                {"search_string": "%" + searchString + "%"})

        cur.execute("""SELECT search_string FROM geodata.search_index_v
                          """
                    )
        # cur.execute(room_query)
        room_nums = cur.fetchall()

        room_num_list = []
        for x in room_nums:
            v = x[0]
            room_num_list.append(v)

        try:
            # return Response(room_num_list)
            return HttpResponse(json.dumps(room_num_list), content_type='application/json')
        except:
            logger.error("error exporting to json model: " + str(room_num_list))
            logger.error(traceback.format_exc())
            return Response({'error': 'either no JSON or no key params in your JSON'})


@api_view(['GET'])
def space_centroid(request, space_id):

    space_qs = BuildingFloorSpace.objects.filter(pk=space_id)

    if space_qs:
        att = space_qs.values()[0]

        if att['multi_poly']:
            att['multi_poly'] = None

        centroid_res = BuildingFloorSpace.objects.annotate(json=AsGeoJSON(Centroid('multi_poly'))).get(pk=space_id).json

        res = Feature(geometry=json.loads(centroid_res), properties=att)

        return Response(res)
    else:
        return Response(
            {'error': 'Sorry we did not find any record in our database matching your id = ' + str(space_id)})
