from django.conf.urls import url
from django.urls import path, include
from poi_manager.views import poi_category_list, poi_category_json, search_poi_by_name, \
    poi_json_tree, poi_root_nodes, get_poi_by_cat_id

from poi_manager.viewsets import PoiCategoryViewSet, PoiViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'category', PoiCategoryViewSet, basename='poi')
router.register(r'', PoiViewSet)


urlpatterns = [
               url(r'^category-list/$', poi_category_list, name='category-list'),
               url(r'^category-poi/$', poi_category_json, name='category-json'),
               url(r'^tree/$', poi_json_tree, name='js-tree'),
               url(r'^roots/$', poi_root_nodes, name='tree-roots'),
               url(r'^cat/(?P<cat_id>\d{1,6})/$', get_poi_by_cat_id, name='get_poi_by_catid'),
               url(r'^search/(?P<poi_name>.+)', search_poi_by_name, name='poi by name'),
               path('', include(router.urls)),
               # url(r'^jstree/demo/$', poi_bootstrap_tree, name='bootstrap-tree'),
               # url(r'^list/$', poi_list, name='list all pois'),
               # url(r'^(?P<poi_id>\d{0,6})/$', get_poi_by_id, name='get poi by id'),

               # url(r'^category/(?P<cat_id>\d{1,6})/$', get_poicat_by_id, name='get poi category'),
               # url(r'^category/(?P<category_name>.+)/$', poi_category_by_name, name='list categories by name'),
               # url(r'^name/(?P<category_name>.+)/$', get_poi_by_cat_name, name='search_poi_by_category'),


]

# urlpatterns = format_suffix_patterns(urlpatterns)
