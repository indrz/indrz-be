from rest_framework import serializers
from buildings.models import Building, BuildingFloorSpace, LtSpaceType, BuildingFloor
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('id', 'building_name', 'num_floors')


class BuildingFloorSpaceSerializer(GeoFeatureModelSerializer):
    fk_building = BuildingSerializer(read_only=True)

    class Meta:
        model = BuildingFloorSpace
        geo_field = "multi_poly"
        fields = ('id', 'short_name', 'floor_num', 'multi_poly', 'fk_building', 'fk_building_floor',
                  'room_external_id', 'space_type')


class BuildingFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingFloor
        fields = ('id', 'short_name', 'floor_num', 'fk_building')
