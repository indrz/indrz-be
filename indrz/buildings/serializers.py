from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Campus, Building, BuildingFloorSpace, BuildingFloor, Organization


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('id', 'name', 'description')


class CampusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campus
        fields = ('id', 'campus_name', 'description', 'fk_organization', 'centroid')
        # depth = 1  # include organization information


class CampusLocationsSerializer(GeoFeatureModelSerializer):
    buildings = serializers.StringRelatedField(many=True)

    class Meta:
        model = Campus
        geo_field = 'geom'
        fields = ('id', 'campus_name', 'description', 'fk_organization', 'buildings' )

# class ItemSerializer(serializers.ModelSerializer):
#     category_name = serializers.RelatedField(source='category', read_only=True)
#
#     class Meta:
#         model = Item
#         fields = ('id', 'name', 'category_name')


class BuildingFloorSpaceSerializer(GeoFeatureModelSerializer):
    building_name = serializers.StringRelatedField(source='fk_building', read_only=True)
    floor_name = serializers.StringRelatedField(source='fk_building_floor', read_only=True)
    type_name = serializers.StringRelatedField(source='space_type', read_only=True)

    class Meta:
        model = BuildingFloorSpace
        geo_field = "multi_poly"
        fields = ('id', 'short_name', 'floor_num', 'room_code', 'multi_poly', 'fk_building', 'fk_building_floor',
                  'room_external_id', 'space_type', 'building_name', 'floor_name', 'type_name')

class BuildingFloorGeomSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = BuildingFloor
        geo_field = 'multi_poly'
        fields = ('id', 'short_name', 'floor_num', 'fk_building')


class FloorSerializerOld(serializers.ModelSerializer):
    buildingfloorspace_set = BuildingFloorSpaceSerializer(many=True, read_only=True)

    class Meta:
        model = BuildingFloor
        fields = ('id', 'short_name', 'floor_num', 'fk_building', 'buildingfloorspace_set')


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingFloor
        fields = ('id', 'short_name', 'floor_num', 'fk_building')


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ('id', 'building_name', 'num_floors', 'fk_organization', 'fk_campus')

class BuildingSerializerDetails(serializers.ModelSerializer):

    buildingfloor_set = FloorSerializerOld(many=True, read_only=True)

    class Meta:
        model = Building
        fields = ('id', 'building_name', 'num_floors', 'buildingfloor_set')

class FloorSerializerDetails(serializers.ModelSerializer):

    buildingfloorspace_set = BuildingFloorSpaceSerializer(many=True, read_only=True)

    class Meta:
        model = BuildingFloor
        fields = ('id', 'short_name', 'floor_num', 'fk_building', 'buildingfloorspace_set')


class SpaceSerializer(GeoFeatureModelSerializer):
    fk_building = BuildingSerializer(read_only=True)
    fk_building_floor = BuildingFloorGeomSerializer(read_only=True)

    class Meta:
        model = BuildingFloorSpace
        geo_field = "multi_poly"
        fields = ('id', 'short_name', 'floor_num', 'multi_poly', 'fk_building', 'fk_building_floor',
                  'room_external_id', 'space_type')


class FloorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuildingFloor
        fields = ('id', 'short_name', 'floor_num')


class CampusFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingFloor
        fields = ('floor_num', 'short_name')
