from django.http import HttpResponse
from django.shortcuts import render


def route_map(request, map_name):
    return render(request, 'route-map.html')


def zoom_campus(request, campus_id, zoom_level=17):
    """
    Zoom to a specific indoor space such as an office
    :return:
    """
    pass


def zoom_building(request, building_id, zoom_level=18):
    """
    Zoom to a specific building
    :return:
    """
    pass


def zoom_space(request, space_id, zoom_level=20):
    """
    Zoom to a specific indoor space such as an office
    :return:
    """
    pass


def index(request):
    return render(request, 'route-map.html')
