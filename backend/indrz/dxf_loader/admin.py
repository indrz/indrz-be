from django.contrib import admin
from .models import FileRegistry, GeorefParams, DxfLayer, DxfImportedTable
from django.contrib.gis import admin as gis_admin
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.admin import OSMGeoAdmin
from django.forms import Textarea
from django.contrib.postgres.fields import ArrayField


class GeorefParamsAdmin(OSMGeoAdmin):
    list_display = ('table_raw', 'x_org', 'y_org', 'x_geo', 'y_geo', 'scale', 'rotate')
    search_fields = ('table_raw',)
    list_filter = ('table_raw',)
    list_editable = ('x_org', 'y_org', 'x_geo', 'y_geo', 'scale', 'rotate')
    list_per_page = 50
    default_lat = 6142422.265
    default_lon = 1826567.891
    default_zoom = 16

class FileRegistryAdmin(admin.ModelAdmin):
    search_fields = ('table_raw', )
    list_display = ('path', 'table_raw', 'building', 'mtime', 'updated_at', 'building_code', 'floor_name', 'floor_number')


class DxfLayerAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ArrayField: {'widget': Textarea(attrs={'rows': 10, 'cols': 45})},
    }

    def names_display(self, obj):
        return ", ".join(obj.names) if obj.names else ""
    names_display.short_description = 'Names'

    list_display = ('names_display', 'file_registry_table_raw', 'type', 'updated_at')

    def file_registry_table_raw(self, obj):
        return obj.FileRegistry.table_raw if hasattr(obj, 'FileRegistry') and obj.FileRegistry else None
    file_registry_table_raw.short_description = 'FileRegistry File Name'
    list_editable = ('type',)

admin.site.register(FileRegistry, FileRegistryAdmin)
admin.site.register(GeorefParams, GeorefParamsAdmin)
admin.site.register(DxfLayer, DxfLayerAdmin)
admin.site.register(DxfImportedTable)