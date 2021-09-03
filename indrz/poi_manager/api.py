import collections

from mptt.templatetags.mptt_tags import cache_tree_children
from poi_manager.models import PoiCategory, Poi, PoiIcon
from poi_manager.serializers import PoiSerializer, PoiCategorySerializer, PoiIconSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


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
    A simple ViewSet for viewing and editing the POI Categories
    """
    queryset = PoiCategory.objects.all()
    serializer_class = PoiCategorySerializer

    def get_queryset(self):
        return PoiCategory.objects.filter(enabled=True)


def poi_json_tree(request, campus_id, format=None):

    lang_code = request.LANGUAGE_CODE

    def recursive_node_to_dict(node):
        result = collections.OrderedDict()
        result['id'] = node.pk
        if lang_code == "de":
            name = node.cat_name_de
        elif lang_code == "en":
            name = node.cat_name_en
        result['name'] = name
        result['icon'] = node.icon_css_name
        result['selectedIcon'] = node.icon_css_name + "_active"

        if node.pk in (1,2,3,4,5):
            result['selectable'] = False
        # result['state'] = {"checked": False, "disabled": True, "expanded": False, "selected": False}

        children = [recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            result['children'] = children
        return result

    root_nodes = cache_tree_children(PoiCategory.objects.filter(enabled=True))
    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n))

    return Response(dicts)


class PoiIconViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the POI Icons
    """
    queryset = PoiIcon.objects.all()
    serializer_class = PoiIconSerializer
