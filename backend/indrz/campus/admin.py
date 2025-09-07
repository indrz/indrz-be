from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Campus

# Register your models here.
@admin.register(Campus)
class CampusAdmin(OSMGeoAdmin):
    default_lon = 1587954  # Default longitude in map units
    default_lat = 5879516  # Default latitude in map units
    default_zoom = 15  # Default zoom level
    pass