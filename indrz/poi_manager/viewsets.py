import collections

from django.utils.translation import get_language_from_request
from mptt.templatetags.mptt_tags import cache_tree_children
from poi_manager.models import PoiCategory, Poi
from poi_manager.serializers import PoiSerializer, PoiCategorySerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


class PoiViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """
    queryset = Poi.objects.all()
    serializer_class = PoiSerializer
    # search_fields = ('name',)  #  or  'category__cat_name'

    # def get_queryset(self):
    #     return Poi.objects.filter(enabled=True)

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
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """
    queryset = PoiCategory.objects.all()
    serializer_class = PoiCategorySerializer

    def get_queryset(self):
        return PoiCategory.objects.filter(enabled=True)


def poi_json_tree(request, campus_id, format=None):

    lang_code = get_language_from_request(request)

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



# class PoiCategoryViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for viewing accounts.
#     """
#
#     def retrieve(self, request, category_name, pk=None):
#         print(request.data)
#         try:
#             cats = PoiCategory.objects.filter(enabled=True).get(cat_name__contains=category_name)
#             if cats:
#
#                 queryset = Poi.objects.filter(category=cats.id).filter(enabled=True)
#                 if queryset:
#                     serializer_class = PoiSerializer(queryset, many=True)
#
#         except Exception as e:
#             raise APIException(detail=e)
#
#         pass

#

# class ListableViewMixin(object):
#     def get_serializer(self, instance=None, data=None, many=False, *args, **kwargs):
#         return super(ListableViewMixin, self).get_serializer(
#             instance=instance, data=data, many=isinstance(instance, list) or isinstance(data, list),
#             *args, **kwargs)
#  https://stackoverflow.com/questions/22881067/django-rest-framework-post-array-of-objects

# class PoiViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
#     """
#     ViewSet create and list books
#
#     Usage single : POST
#     {
#         "name":"Killing Floor: A Jack Reacher Novel",
#         "author":"Lee Child"
#     }
#
#     Usage array : POST
#     [{
#         "name":"Mr. Mercedes: A Novel (The Bill Hodges Trilogy)",
#         "author":"Stephen King"
#     },{
#         "name":"Killing Floor: A Jack Reacher Novel",
#         "author":"Lee Child"
#     }]
#     """
    # queryset = Poi.objects.all()
    # serializer_class = PoiSerializer
    # search_fields = ('name',)
    #
    # def create(self, request, *args, **kwargs):
    #     """
    #     #checks if post request data is an array initializes serializer with many=True
    #     else executes default CreateModelMixin.create function
    #     """
    #     is_many = isinstance(request.data, list)
    #     if not is_many:
    #         return super(PoiViewSet, self).create(request, *args, **kwargs)
    #     else:
    #         serializer = self.get_serializer(data=request.data, many=True)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
