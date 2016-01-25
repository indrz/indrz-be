from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from poi_manager.models import PoiCategory, Poi

admin.site.register(Poi)
admin.site.register(PoiCategory, MPTTModelAdmin)