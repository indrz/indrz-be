from bookway.models import BookShelf, ShelfData
from django.contrib.gis import admin

class BookShelfAdmin(admin.OSMGeoAdmin):
    list_display = ('external_id', 'left_from_label', 'left_to_label',
                    'right_from_label','right_to_label')
    search_fields = ('external_id', 'left_from_label', 'left_to_label', 'right_from_label', 'right_to_label')
    list_editable = ('left_from_label', 'left_to_label', 'right_from_label', 'right_to_label')
    list_per_page = 50
    default_lat = 5879622.26
    default_lon = 1587955.07
    default_zoom = 20

class ShelfDataAdmin(admin.OSMGeoAdmin):
    list_display = ('external_id', 'section_length', 'section', 'section_main',
                    'system_from', 'system_to', 'measure_from', 'measure_to', 'side', 'bookshelf', 'building_floor')
    search_fields = ('external_id', 'section_main', 'section_child', 'system_from', 'system_to')
    list_filter = ('external_id', 'section_main', 'section_child',)
    list_editable = ('system_from', 'system_to')
    list_per_page = 50
    default_lat = 5879622.26
    default_lon = 1587955.07
    default_zoom = 20

admin.site.register(ShelfData, ShelfDataAdmin)
admin.site.register(BookShelf, BookShelfAdmin)
