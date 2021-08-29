from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin
from poi_manager.models import PoiCategory, Poi, PoiIcon

class PoiAdmin(OSMGeoAdmin):
    list_display = ('id', 'name', 'name_de', 'name_en', 'category', 'image_preview', 'enabled')
    search_fields = ('name', 'category')
    list_filter = ('category', )
    readonly_fields = ('image_preview',)
    default_lat = 5879660.89
    default_lon = 1588005.35
    default_zoom = 16

    def image_preview(self, obj):
        if obj.category.fk_poi_icon.icon.url:
            return mark_safe('<img src="{0}" width="25" height="32" style="object-fit:contain" />'.format(obj.category.fk_poi_icon.icon.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'

class PoiCatAdmin(DraggableMPTTAdmin):
    search_fields = ('cat_name',)
    list_filter = ('cat_name', 'enabled')

class PoiIconAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'icon', 'image_preview')
    fields = ('name', 'icon', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.icon:
            return mark_safe('<img src="{0}" width="25" height="32" style="object-fit:contain" />'.format(obj.icon.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'

admin.site.register(Poi, PoiAdmin)
admin.site.register(PoiIcon, PoiIconAdmin)
admin.site.register(PoiCategory, PoiCatAdmin)
