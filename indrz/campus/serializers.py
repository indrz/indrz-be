from rest_framework import serializers
from campus.models import Campus
from rest_framework_gis.serializers import GeoFeatureModelSerializer
import json

class CampusSerializer(serializers.ModelSerializer):
    extent = serializers.SerializerMethodField()

    def get_extent(self, obj):
        return list(obj.geom.extent)
    
    class Meta:
        model = Campus
        geo_field = 'geom'
        fields = ('id', 'name', 'description', 'fk_organization', 'centroid', 'extent')
        # depth = 1  # include organization information


class CampusSearchSerializer(GeoFeatureModelSerializer):
    name = serializers.SerializerMethodField()
    floor_num = serializers.SerializerMethodField()
    centroid = serializers.SerializerMethodField()

    def get_name(self, Campus):
        return "Campus " + Campus.name

    def get_floor_num(self, Campus):
        floor = 0
        return floor

    def get_centroid(self, Campus):
        center_coord_geom  = json.loads(Campus.geom.centroid.geojson)
        return center_coord_geom

    class Meta:
        model = Campus
        geo_field = 'centroid'
        fields = ('id', 'name', 'floor_num', 'name', 'description', 'fk_organization', 'centroid')
        depth = 1  # include organization information