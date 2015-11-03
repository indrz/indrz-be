from django.contrib import admin
from django.contrib.gis import admin as gis_admin

from buildings.models import LtAccessType, LtSpaceType, LtCondition
from buildings.models import  Organization, Campus, Building
from buildings.models import  BuildingFloor, BuildingFloorSpace, InteriorFloorSection
from routing.models import Networklines


admin.site.register(Organization, gis_admin.OSMGeoAdmin)
admin.site.register(Campus, gis_admin.OSMGeoAdmin)
admin.site.register(Building, gis_admin.OSMGeoAdmin)
admin.site.register(BuildingFloor, gis_admin.OSMGeoAdmin)
admin.site.register(BuildingFloorSpace, gis_admin.OSMGeoAdmin)
admin.site.register(InteriorFloorSection, gis_admin.OSMGeoAdmin)
admin.site.register(Networklines, gis_admin.OSMGeoAdmin)

admin.site.register(LtAccessType)
admin.site.register(LtSpaceType)
admin.site.register(LtCondition)