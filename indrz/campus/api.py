from campus.serializers import CampusSerializer
from campus.models import Campus
from rest_framework import viewsets

class CampusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return a list of campuse
    """
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer