from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from api.search_tu import search_any, searchAutoComplete
from rest_framework_swagger.views import get_swagger_view

from .routers import router

##############################################
# Default
##############################################

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='INDRZ API')

admin.site.site_header = 'INDRZ Manager'

urlpatterns = [
    path('api/v1/api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),
    url(r'^api/v1/docs/$', schema_view),
    url(r'^api/v1/autocomplete/(?P<search_text>.+)', searchAutoComplete.as_view(), name='search_autocomplete'),
    url(r'^api/v1/search/(?P<q>.+)', search_any, name='search'),
    url(r'^api/v1/directions/', include(('routing.urls', 'directions'), namespace='directions')),
    url(r'^api/v1/admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
    path('api/v1/api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),
    path('', include(('homepage.urls', 'homepage'), namespace='homepage'))
]


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^translate/', include('rosetta.urls')),
    ]


# from api import search
# from buildings.views import get_spaces_on_floor, campus_list, campus_buildings_list, campus_buildings_short_list, \
#     space_details, get_campus_info, campus_floor_spaces, campus_locations
# from django.conf.urls import url, include
# from rest_framework.documentation import include_docs_urls
#
# from .search_aau import AauApi
# from .views import get_campus_floors, get_room_center
#
# # SPACES API URLS
# urlpatterns = [
#     # url(r'^spaces/$', 'spaces_list', name='list_all_campuses'),
#     url(r'^getcenter/(?P<big_pk>(\d{3}_\d{2}_[A-Z]{1}[A-Z0-9]{1}[0-9]{2}_\d{6}))/$', get_room_center,
#         name='show_space_details'),
#     url(r'^spaces/(?P<space_id>\d{1,5})/$', space_details, name='show_space_details'),
# ]
#
# # Floors API URLS
# urlpatterns += [
#     url(r'^floors/(?P<floor_id>\d{1,5})/$', get_spaces_on_floor, name='get_spaces_on_floor'),
# ]
#

#
# urlpatterns += [
#
#     url(r'^campus/(?P<campus_id>\d{1,5})/poi/', include('poi_manager.urls')),
#
# ]
#
# # urlpatterns += [
#     # url(r'^$', view_map, name='map_home'),
#     #             url(r'^autocomplete/(?P<search_text>.+)', searchAutoComplete.as_view(), name='search_autocomplete'),
#                 # url(r'^search/(?P<q>.+)', search_any, name='search'),
#                 # url(r'^map/(?P<poicatid>poi-cat-id=\d{1,4})(,\d{1,4})?(,\d{1,4})?(,\d{1,4})?(,\d{1,4})?', view_map, name='map_name'),
#                 # url(r'^map/(?P<map_name>[^/]+)/$', view_map, name='map_name'),
#                 # url(r'^help/$', view_help, name='help'),
#                 # url(r'^aausearch/(?P<q>.+)', AauApi.as_view(), name='aau search')]
#
# # DIRECTIONS API URLS
# urlpatterns += [
#     url(r'^directions/', include('routing.urls')),
#     url(r'^search/.+', AauApi.as_view(), name='aau search')
# ]
#
# urlpatterns += [
#     url(r'^campus/(?P<campus_id>\d{1,5})/poi/', include('poi_manager.urls')),
#     # url(r'^docs/', include_docs_urls(title='Indrz API docs', patterns=doc_urls, public=False)),
# ]
#
# # http://localhost:8000/api/v1/directions/force_mid/?startnode=1385&midnode=1167&endnode=1252
# # http://localhost:8000/api/v1/directions/buildingid=1&startid=307: Orne&endid=311: Mayenne
# # http://localhost:8000/api/v1/directions/buildingid=1&startid=1173&endid=1231



##############################################
# Static and media files in debug mode
##############################################

# if settings.DEBUG:
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
#     def mediafiles_urlpatterns(prefix):
#         """
#         Method for serve media files with runserver.
#         """
#         import re
#         from django.views.static import serve
#
#         return [
#             url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), serve,
#                 {'document_root': settings.MEDIA_ROOT})
#         ]
#
#     # Hardcoded only for development server
#     urlpatterns += staticfiles_urlpatterns(prefix="/static/")
#     urlpatterns += mediafiles_urlpatterns(prefix="/media/")


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url('__debug__/', include(debug_toolbar.urls)),
#
#     ] + urlpatterns
