from django.contrib import admin
from django.contrib.gis import admin as gis_admin

from buildings.models import LtAccessType, LtSpaceType, LtCondition
from buildings.models import  Organization, Campus, Building
from buildings.models import  BuildingFloor, BuildingFloorSpace, InteriorFloorSection

from buildings.models import Wing

admin.site.register(Organization, gis_admin.OSMGeoAdmin)
admin.site.register(Campus, gis_admin.OSMGeoAdmin)
admin.site.register(InteriorFloorSection, gis_admin.OSMGeoAdmin)

class LtSpaceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('name',)


class BuildingFloorSpaceAdmin(gis_admin.OSMGeoAdmin):
    list_display = ('short_name', 'room_external_id', 'room_code', 'room_description', 'tag', 'fk_building_floor', 'floor_num', 'space_type', 'id')
    search_fields = ('short_name', 'room_external_id', 'room_code', 'room_description', 'tag')
    list_filter = ('fk_building_floor__fk_building__fk_campus__campus_name', 'floor_num', 'fk_building_floor__short_name')
    default_lat = 6139956.30
    default_lon = 1822274.03
    default_zoom = 16


class BuildingFloorAdmin(gis_admin.OSMGeoAdmin):
    list_display = ('short_name', 'fk_building', 'id')
    search_fields = ('short_name',)
    default_lat = 6139956.30
    default_lon = 1822274.03
    default_zoom = 16


class BuildingAdmin(gis_admin.OSMGeoAdmin):
    list_display = ('name', 'building_name', 'wings','street', 'description', 'fk_campus', 'fk_organization', 'id')
    search_fields = ('building_name', 'street', 'description', 'wings')
    list_filter = ('fk_campus__campus_name',)
    default_lat = 6139956.30
    default_lon = 1822274.03
    default_zoom = 16

class WingAdmin(gis_admin.OSMGeoAdmin):
    list_display = ('name', 'abbreviation', 'id')
    search_fields = ('name','abbreviation',)
    default_lat = 6139956.30
    default_lon = 1822274.03
    default_zoom = 16


admin.site.register(LtAccessType)
admin.site.register(LtSpaceType, LtSpaceTypeAdmin)
admin.site.register(LtCondition)

admin.site.register(Building, BuildingAdmin )
admin.site.register(BuildingFloor, BuildingFloorAdmin )
admin.site.register(BuildingFloorSpace, BuildingFloorSpaceAdmin)
admin.site.register(Wing, WingAdmin )
