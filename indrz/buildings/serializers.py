import json

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Campus, Building, BuildingFloorSpace, BuildingFloor, Organization, Wing


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('id', 'name', 'description')


class CampusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campus
        geo_field = 'geom'
        fields = ('id', 'campus_name', 'description', 'fk_organization', 'centroid')
        # depth = 1  # include organization information


class BuildingFloorSpaceSerializer(GeoFeatureModelSerializer):
    building_name = serializers.StringRelatedField(source='fk_building', read_only=True)
    floor_name = serializers.SerializerMethodField()
    type_name = serializers.StringRelatedField(source='space_type', read_only=True)
    name = serializers.SerializerMethodField()
    category_en = serializers.SerializerMethodField()
    category_de = serializers.SerializerMethodField()
    wing = serializers.SerializerMethodField()


    def get_building_name(self, BuildingFloorSpace):
        return BuildingFloorSpace.fk_building.building_name
    def get_floor_name(self, BuildingFloorSpace):
        return BuildingFloorSpace.floor_name
        # TODO fix data so we can use fk_building_floor
        # return BuildingFloorSpace.fk_building_floor.floor_name

    def get_name(self, BuildingFloorSpace):
        name = ""

        if BuildingFloorSpace.short_name:
            name = BuildingFloorSpace.short_name
        else:
            if BuildingFloorSpace.room_code:
                name = BuildingFloorSpace.room_code

        return name

    def get_category_en(self, BuildingFloorSpace):
        # return BuildingFloorSpace.
        return ""

    def get_category_de(self, BuildingFloorSpace):
        return ""
        # return BuildingFloorSpace.long_name

    def get_wing(self, BuildingFloorSpace):
        wing = ""
        if BuildingFloorSpace.room_code:
            wing = BuildingFloorSpace.room_code[:2]
        return wing

    class Meta:
        model = BuildingFloorSpace
        geo_field = "geom"
        fields = ('id', 'short_name', 'long_name', 'name', 'floor_num', 'room_code', 'geom',
                  'fk_building', 'building_name', 'fk_building_floor',
                  'room_external_id', 'room_description', 'space_type',  'floor_name', 'type_name',
                  'category_en', 'category_de', 'capacity', 'wing')

        read_only_fields = ('centerGeometry',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['properties']['id'] = representation['id']
        representation['properties']['space_type_id'] = representation['properties']['space_type']
        representation['properties']['src_icon'] = "space"
        return representation

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


class BuildingSerializer(GeoFeatureModelSerializer):
    name = serializers.SerializerMethodField()
    floor_num = serializers.SerializerMethodField()
    abbreviation = serializers.SerializerMethodField()
    floor_list = serializers.SerializerMethodField()

    def get_floor_list(self, Building):
        distinct_floors = BuildingFloor.objects.filter(fk_building=Building.id).values_list('floor_num', flat=True).distinct()
        return distinct_floors

    def get_floor_num(self, Building):

        return 0


    def get_name(self, Building):
        return  Building.building_name + " (" + Building.name + ")"


    def get_abbreviation(self, Building):
        return Building.name

    class Meta:
        model = Building
        geo_field = "geom"
        fields = ('id', 'building_name', 'name', 'abbreviation', 'floor_num', 'fk_campus', 'wings', 'floor_list',
                  'street', 'postal_code', 'municipality', 'city')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['properties']['id'] = representation['id']
        representation['properties']['src_icon'] = "building"
        return representation

class CampusSearchSerializer(GeoFeatureModelSerializer):
    name = serializers.SerializerMethodField()
    floor_num = serializers.SerializerMethodField()
    centroid = serializers.SerializerMethodField()

    def get_name(self, Campus):
        return "Campus " + Campus.campus_name

    def get_floor_num(self, Campus):
        floor = 0
        return floor

    def get_centroid(self, Campus):
        center_coord_geom  = json.loads(Campus.geom.centroid.geojson)
        return center_coord_geom

    class Meta:
        model = Campus
        geo_field = 'centroid'
        fields = ('id', 'name', 'floor_num', 'campus_name', 'description', 'fk_organization', 'centroid')
        depth = 1  # include organization information


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['properties']['id'] = representation['id']
        representation['properties']['src_icon'] = "space"
        return representation


class FloorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuildingFloor
        fields = ('id', 'short_name', 'floor_num')


class CampusFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingFloor
        fields = ('floor_num', 'short_name')


class WingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wing
        fields = ('id', 'short_name', 'long_name', 'floor_num', 'floor_name', 'name', 'abbreviation',
                  'fk_building_id', 'fk_building_floor_id')