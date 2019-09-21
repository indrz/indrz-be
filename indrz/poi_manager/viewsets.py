from rest_framework import viewsets
from rest_framework.exceptions import APIException

from poi_manager.models import PoiCategory, Poi
from poi_manager.serializers import PoiSerializer


class PoiCategoryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for viewing accounts.
    """

    def retrieve(self, request, category_name, pk=None):
        print(request.data)
        try:
            cats = PoiCategory.objects.filter(enabled=True).get(cat_name__contains=category_name)
            if cats:

                queryset = Poi.objects.filter(fk_poi_category=cats.id).filter(enabled=True)
                if queryset:
                    serializer_class = PoiSerializer(queryset, many=True)

        except Exception as e:
            raise APIException(detail=e)

        pass


