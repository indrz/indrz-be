from buildings.models import BuildingFloor, Campus
from buildings.serializers import FloornewSerializer, CampusSerializer, BuildingSerializer
from rest_framework import viewsets


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


class BuildingsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
