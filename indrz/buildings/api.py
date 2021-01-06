from buildings.models import BuildingFloor, Campus, Building
from buildings.serializers import FloorSerializer, CampusSerializer, BuildingSerializer
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
    serializer_class = FloorSerializer


class BuildingsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
