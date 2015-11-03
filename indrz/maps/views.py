from django.http import HttpResponse
from django.shortcuts import render


def route_map(request, map_name):
    return render(request, 'route-map.html')


def index(request):
    return render(request, 'route-map.html')
