from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from buildings.models import BuildingFloorSpace, Building, Campus
from buildings.serializers import BuildingFloorSpaceSerializer, BuildingSerializer, CampusSerializer
from poi_manager.models import Poi
from poi_manager.serializers import PoiSerializer



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def share_result(request, id, type='poi'):
    '''
    Find poi, space, zone to share
    '''

    d = request.data
    print("oh data......", d)


    if type == 'space':
        try:
            space = BuildingFloorSpace.objects.get(room_code=id)

            s = BuildingFloorSpaceSerializer(space)
            return Response(s.data)
        except:
            return Response("no space found", status=400)

    if type == 'poi':
        try:
            poi = Poi.objects.get(id=id)
            p =PoiSerializer(poi)
            return Response(p.data)
        except:
            return Response("no poi found", status=400)

    if type == 'building':
        try:
            building = Building.objects.get(id=id)
            b = BuildingSerializer(building)
            return Response(b.data)
        except:
            return Response("no building found", status=400)

    if type == 'campus':
        try:
            campus = Campus.objects.get(id=id)
            c = CampusSerializer(campus)
            return Response(c.data)
        except:
            return Response("no campus found", status=400)

