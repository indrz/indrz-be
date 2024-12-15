from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from poi_manager.models import PoiCategory, Poi, PoiIcon, PoiImages
from poi_manager.serializers import PoiSerializer, PoiCategorySerializer, PoiIconSerializer, PoiImageSerializer


class PoiViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the POI
    """
    queryset = Poi.objects.all()
    serializer_class = PoiSerializer
    # search_fields = ('name',)  #  or  'category__cat_name'

    def get_queryset(self):
        return Poi.objects.filter(enabled=True)

    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(PoiViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    # permission_classes = [IsAccountAdminOrReadOnly]


class PoiCategoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the POI Category
    """
    queryset = PoiCategory.objects.all()
    serializer_class = PoiCategorySerializer

    def get_queryset(self):
        return PoiCategory.objects.filter(enabled=True)


class PoiIconViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the POI Icons
    """
    queryset = PoiIcon.objects.all()
    serializer_class = PoiIconSerializer

class PoiImageViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing POI Images.
    """
    queryset = PoiImages.objects.all()
    serializer_class = PoiImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data

        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
