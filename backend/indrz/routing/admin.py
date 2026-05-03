from django.contrib.gis import admin

from .models import RoutingEdge


@admin.register(RoutingEdge)
class RoutingEdgeAdmin(admin.OSMGeoAdmin):
    list_display = (
        "id",
        "campus",
        "building",
        "floor_from",
        "floor_to",
        "line_type",
        "is_private",
        "created_at",
        "updated_at",
    )
    list_filter = ("campus", "building", "line_type", "is_private")
    search_fields = ("id",)
    default_lon = 1587954  # Default longitude in map units
    default_lat = 5879516  # Default latitude in map units
    default_zoom = 15  # Default zoom level

# Register your models here.
