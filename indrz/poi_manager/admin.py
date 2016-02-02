from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from poi_manager.models import PoiCategory, Poi, PoiIcon

admin.site.register(Poi)
admin.site.register(PoiIcon)
admin.site.register(PoiCategory, MPTTModelAdmin)