import uuid

from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.shortcuts import redirect, get_object_or_404
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin
from poi_manager.models import PoiCategory, Poi, PoiIcon, PoiImages
from pathlib import Path
from PIL import Image as Pilimage
from django.core.files.base import ContentFile
from io import BytesIO

class PoiAdmin(OSMGeoAdmin):
    list_display = ('id', 'name', 'name_de', 'name_en', 'category', 'poi_images_preview', 'icon_preview', 'enabled', 'html_content')
    list_editable = ('name', 'name_de', 'name_en', 'html_content', 'enabled')
    search_fields = ('name',)
    list_filter = ('category', )
    readonly_fields = ('icon_preview', 'poi_images_preview')
    default_lat = 6139956.30
    default_lon = 1822274.03
    default_zoom = 16
    list_per_page = 25

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
                if img.image:
                    html_elements.append(f'<a href="{img.image.url}"><img src="{img.image.url}" width="150" height="80" style="object-fit:contain" /></a>')
                    return mark_safe("".join(html_elements))
                else:
                    return '(no images)'
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
    search_fields = ('poi__name', )
    list_display = ('id', 'poi', 'image_preview', 'image', 'sort_order', 'alt_text')
    list_editable = ('sort_order', 'alt_text')
    readonly_fields = ('image_preview', 'thumbnail')
    list_select_related = ('poi',)  # Optimizes poi join query
    list_per_page = 15
    actions = ['rotate_image']

    def rotate_image(self, request, queryset):
        for obj in queryset:
            # Open the image file
            img = Pilimage.open(obj.image.path)

            # Rotate the image 90 degrees to the right
            rotated_image = img.rotate(-90, expand=True)

            # Generate a new hash for the filename
            new_hash = uuid.uuid4().hex[:8]

            # Extract the original filename and extension
            original_name = Path(obj.image.name).stem.split('_')[0]
            file_suffix = Path(obj.image.name).suffix

            # Construct the new filename
            new_filename = f"{original_name}_{new_hash}{file_suffix}"

            # Save the rotated image with the new filename
            rotated_image.save(Path(obj.image.path).parent / new_filename)

            # Re-open the image to update the file object in the model
            with open(Path(obj.image.path).parent / new_filename, 'rb') as f:
                obj.image.save(new_filename, ContentFile(f.read()), save=False)

            # Recreate and save the thumbnail if necessary
            rotated_image.thumbnail((400, 250), Pilimage.ANTIALIAS)
            temp_thumb = BytesIO()
            rotated_image.save(temp_thumb, format='JPEG')
            temp_thumb.seek(0)

            thumb_filename = f"{original_name}_thumbnail_{new_hash}{file_suffix}"

            obj.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)

            # Save the model instance to update the thumbnail and any other changes
            obj.save()

        # Redirect back to the change form after rotation
        self.message_user(request, "Selected images rotated by 90 degrees.")
        return redirect(request.META['HTTP_REFERER'])

    rotate_image.short_description = "Rotate selected images 90° Right"

    def get_queryset(self, request):
        # Use select_related or prefetch_related to optimize database queries
        qs = super().get_queryset(request)
        return qs.select_related('poi')  # Assuming poi is a ForeignKey

    def image_preview(self, obj):

        if obj.image:
            return mark_safe('<a href="{0}"><img src="{0}" width="150" height="80" style="object-fit:contain" /></a>'.format(obj.image.url))
        else:
            return '(no image)'

    image_preview.short_description = 'Preview'

admin.site.register(Poi, PoiAdmin)
admin.site.register(PoiIcon, PoiIconAdmin)
admin.site.register(PoiCategory, PoiCatAdmin)
admin.site.register(PoiImages, PoiImageAdmin)
