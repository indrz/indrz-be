from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from poi_manager.models import PoiCategory, Poi, PoiIcon


class PoiAdmin(OSMGeoAdmin):
    list_display = ('id', 'name', 'name_de', 'name_en', 'category', 'enabled')
    search_fields = ('name', 'category')
    list_filter = ('category', )
    default_lat = 5879660.89
    default_lon = 1588005.35
    default_zoom = 16

class PoiCatAdmin(DraggableMPTTAdmin):
    search_fields = ('cat_name',)
    list_filter = ('cat_name', 'enabled')


class PoiIconAdmin(admin.ModelAdmin):
    list_display = ('name', 'pictogram_img',)
    fields = ('pictogram_img',)
    readonly_fields = ('pictogram_img',)



admin.site.register(Poi, PoiAdmin)
admin.site.register(PoiIcon, PoiIconAdmin)
admin.site.register(PoiCategory, PoiCatAdmin)
