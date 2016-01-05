from django.shortcuts import render


def route_map(request, *args, **kwargs):
    context = {}
    if request.method == 'GET':
        map_name = kwargs.pop('map_name', None)
        building_id, = request.GET.get('buildingid', 1),
        space_id, = request.GET.get('spaceid', 0),
        zoom_level, = request.GET.get('zoom', 18),

        context.update({
            'map_name': map_name,
            'building_id': building_id,
            'space_id': int(space_id),
            'zoom_level': zoom_level,
        })

    return render(request, context=context, template_name='map.html')
