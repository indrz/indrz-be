from rest_framework.decorators import api_view
from models import Campus
from django.http import HttpResponse
from geojson import Feature, FeatureCollection, Point

from rest_framework.decorators import api_view
from rest_framework.response import Response
import geojson
from django.contrib.gis.geos import GEOSGeometry

# Create your views here.
@api_view(['GET', ])
def campus_locations(request, format=None):
    """
    List locations of all campuses as points

    """

    if request.method == 'GET':

        campuses = Campus.objects.values()
        features = []

        if campuses:

            for campus in campuses:
                atts = {'id': campus['id'], 'campus_name': campus['campus_name']}

                geo = GEOSGeometry(campus['geom']).centroid

                f = Feature(geometry=geojson.loads(geo.geojson), properties=atts)
                features.append(f)

            fc = FeatureCollection(features)

            return Response(fc)
        else:
            return Response({"error": "no campus data found"})