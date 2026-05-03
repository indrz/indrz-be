from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from bookway.models import ShelfData, BookShelf


class ShelfdataSerializer(serializers.ModelSerializer):
    floor_num = serializers.SerializerMethodField()
    def get_floor_num(self, ShelfData):
        return ShelfData.building_floor.floor_num

    class Meta:
        model = ShelfData
        fields = ('id', 'building_floor', 'building', 'external_id', 'section_main', 'section_child',
                  'system_from', 'system_to', 'side', 'measure_from', 'measure_to', 'bookshelf', 'floor_num')


class BookshelfSerializer(GeoFeatureModelSerializer):
    floor_num = serializers.SerializerMethodField()
    floor_name = serializers.SerializerMethodField()
    
    def get_floor_name(self, BookShelf):
        return BookShelf.building_floor.short_name if object.building_floor else None
    
    def get_floor_num(self, BookShelf):
        return BookShelf.building_floor.floor_num if object.building_floor else None
    
    class Meta:
        model = BookShelf
        fields = ('id', 'external_id', 'left_from_label', 'left_to_label', 'right_from_label', 'right_to_label',
                  'double_sided', 'rotation', 'length', 'width', 'depth', 'building', 'building_floor', 'floor_num', 'floor_name')
        geo_field = 'geom'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['properties']['id'] = representation['id']
        representation['properties']['src_icon'] = "book"
        return representation
