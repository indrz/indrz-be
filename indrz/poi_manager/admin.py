from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin
from poi_manager.models import PoiCategory, Poi, PoiIcon, PoiImages

class PoiAdmin(OSMGeoAdmin):
    list_display = ('id', 'name', 'name_de', 'name_en', 'category', 'icon_preview', 'poi_images_preview', 'enabled', 'html_content')
    list_editable = ('name', 'name_de', 'name_en', 'html_content', 'enabled')
    search_fields = ('name',)
    list_filter = ('category', )
    readonly_fields = ('icon_preview', 'poi_images_preview')
    default_lat = 6139956.30
    default_lon = 1822274.03
    default_zoom = 16

    def icon_preview(self, obj):
        icon_url = obj.category.fk_poi_icon.icon.url
        if icon_url:
            return mark_safe('<a href="{0}"><img src="{0}" width="25" height="32" style="object-fit:contain" /></a>'.format(icon_url))
        else:
            return '(No image)'

    icon_preview.short_description = 'POI Icon Preview'

    def poi_images_preview(self, obj):
        poi_images = PoiImages.objects.filter(poi_id=obj.id)

        if poi_images:
            html_elements = []
            for img in poi_images:
                html_elements.append(f'<a href="{img.image.url}"><img src="{img.thumb.url}" width="150" height="80" style="object-fit:contain" /></a>')
            return mark_safe("".join(html_elements))
        else:
            return '(no images)'

    poi_images_preview.short_description = 'POI Images'


class PoiCatAdmin(DraggableMPTTAdmin):
    search_fields = ('cat_name',)
    list_filter = ('cat_name', 'enabled')

class PoiIconAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'icon_preview', 'icon')
    fields = ('name', 'icon', 'icon_preview')
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        if obj.icon:
            return mark_safe('<a href="{0}"><img src="{0}" width="25" height="32" style="object-fit:contain" /></a>'.format(obj.icon.url))
        else:
            return '(No image)'

    icon_preview.short_description = 'Icon Preview'

class PoiImageAdmin(admin.ModelAdmin):
    search_fields = ('poi.name', )
    list_display = ('id', 'poi', 'poi_id', 'image_preview', 'sort_order', 'alt_text')
    list_editable = ('poi', 'alt_text')
    readonly_fields = ('image_preview', 'thumbnail')

    def image_preview(self, obj):
        if obj.thumbnail:
            return mark_safe('<a href="{1}"><img src="{0}" width="150" height="80" style="object-fit:contain" /></a>'.format(obj.thumbnail.url, obj.image.url))
        else:
            return '(no image)'

    image_preview.short_description = 'Preview'

admin.site.register(Poi, PoiAdmin)
admin.site.register(PoiIcon, PoiIconAdmin)
admin.site.register(PoiCategory, PoiCatAdmin)
admin.site.register(PoiImages, PoiImageAdmin)
