from django.urls import re_path, include
from rest_framework import routers
from bookway.views import ShelfdataViewSet, BookshelfViewSet
from bookway.views import book_location, shelf_poly

router = routers.DefaultRouter()
router.register(r'shelfdata', ShelfdataViewSet, basename='shelfdata')
router.register(r'bookshelf', BookshelfViewSet, basename='bookshelf',)

urlpatterns = [
    re_path('', include(router.urls), name='bookshelf_shelfdata'),
    re_path(r'location/(?P<key_value>.+)', book_location, name='book location'),
    re_path(r'shelf/(?P<key_value>.+)', shelf_poly, name='shelf polygon'),
    re_path(r'search/(?P<key_value>.+)', book_location, name='bookway search'),

]