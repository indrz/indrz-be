from django.conf.urls import url
from django.urls import path, include
from poi_manager.views import search_poi_by_name, \
    poi_json_tree, poi_root_nodes, get_poi_by_cat_id

from poi_manager.api import PoiCategoryViewSet, PoiViewSet, PoiIconViewSet, PoiImageViewSet
from rest_framework import routers

poi_router = routers.DefaultRouter()

poi_router.register(r'category', PoiCategoryViewSet, basename='poi')
poi_router.register(r'icon', PoiIconViewSet)
poi_router.register(r'images', PoiImageViewSet)
poi_router.register(r'', PoiViewSet)


urlpatterns = [
               url(r'^tree/$', poi_json_tree, name='js-tree'),
               url(r'^roots/$', poi_root_nodes, name='tree-roots'),
               url(r'^cat/(?P<cat_id>\d{1,6})/$', get_poi_by_cat_id, name='get_poi_by_catid'),
               url(r'^search/(?P<poi_name>.+)', search_poi_by_name, name='poi by name'),
               path('', include(poi_router.urls)),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
