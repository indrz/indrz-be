from django.http import HttpResponse
from django.shortcuts import render


def map_socgen_nantes(request):
    return render(request, 'socgen-nantes.html')


def testswitch(request):
    return render(request, 'testswitch.html')


# def index(request):
#     return render(request, 'route-map.html')
