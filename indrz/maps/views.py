from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

from buildings.models import Building


def route_map(request, *args, **kwargs):
    context = {}
    if request.method == 'GET':
        map_name = kwargs.pop('map_name', None)
        building_id, = request.GET.get('buildingid', 1),
        space_id, = request.GET.get('spaceid', 1),
        zoom_level, = request.GET.get('zoom', 18),

        context.update({
            'map_name': map_name,
            'building_id': building_id,
            'space_id': space_id,
            'zoom_level': zoom_level,
        })

    return render(request, context=context, template_name='map.html')


def map_socgen_nantes(request):
    return render(request, 'socgen-nantes.html')


def testswitch(request):
    return render(request, 'testswitch.html')


# def index(request):
#     return render(request, 'route-map.html')
