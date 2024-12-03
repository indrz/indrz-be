from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from buildings.models import BuildingFloor, Campus, Building, BuildingFloorSpace, Wing
from buildings.serializers import (FloorSerializer, CampusSerializer, BuildingSerializer,
                                   BuildingFloorSpaceSerializer, WingSerializer)


class CampusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return a list of campuse
    """
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer


class FloorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return a list of floors
    """
    queryset = BuildingFloor.objects.order_by('-floor_num').distinct('floor_num')
    serializer_class = FloorSerializer


class BuildingsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Readonly return a list of buildings and floors per building
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    @action(detail=True)
    def floors(self, request, *args, **kwargs):
        instance = self.get_object()
        floor = BuildingFloor.objects.filter(fk_building_id=instance)
        serializer = FloorSerializer(floor, many=True)
        return Response(serializer.data)


class SpaceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return a list of floors
    """
    queryset = BuildingFloorSpace.objects.distinct('room_code')
    serializer_class = BuildingFloorSpaceSerializer


class WingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return a list of floors
    """
    queryset = Wing.objects.all()
    serializer_class = WingSerializer
