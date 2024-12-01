from django.contrib import admin
from django.contrib.gis import admin as gis_admin

from landscape.models import LtSurfaceType, LtAmenityType
from landscape.models import  LandscapeArea, LandscapeAmenityLine


class LtSpaceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('name',)


admin.site.register(LandscapeArea, gis_admin.OSMGeoAdmin)
admin.site.register(LandscapeAmenityLine, gis_admin.OSMGeoAdmin)

admin.site.register(LtAmenityType, LtSpaceTypeAdmin)
admin.site.register(LtSurfaceType, LtSpaceTypeAdmin)
