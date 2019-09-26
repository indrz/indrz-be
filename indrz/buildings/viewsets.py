from rest_framework import viewsets

from buildings.models import BuildingFloor, Campus
from buildings.serializers import FloornewSerializer, CampusSerializer


class CampusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer


class FloorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = BuildingFloor.objects.order_by('-floor_num').distinct('floor_num')
    serializer_class = FloornewSerializer


