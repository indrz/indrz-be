from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from homepage.views import view_map #view_help
from api.search_tu import search_any, searchAutoComplete, TuApi
# all urls begin with http://localhost:8000/map/

urlpatterns = [
    #  ex valid call from to  /api/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2
    # url(r'^(?P<map_name>[0-9a-zA-Z_-]+)/$', 'view_map', name='map_name'),
    # url(r'^', view_map, name='map_name'),
    # /autocomplete/?query=Irene Fellner
    url(r'^$', view_map, name='map_home'),
    url(r'^autocomplete/(?P<search_text>.+)', searchAutoComplete.as_view(), name='search_autocomplete'),
    url(r'^search/(?P<q>.+)', search_any, name='search'),
    # # url(r'^map/(?P<poicatid>poi-cat-id=\d{1,4})(,\d{1,4})?(,\d{1,4})?(,\d{1,4})?(,\d{1,4})?', view_map, name='map_name'),
    # url(r'^map/(?P<map_name>[^/]+)/$', view_map, name='map_name'),
    # url(r'^help/$', view_help, name='help'),
    url(r'^aausearch/(?P<q>.+)', TuApi.as_view(), name='aau search')

]
