from rest_framework import serializers

from .models import Poi, PoiCategory
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class PoiSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Poi
        geo_field = 'geom'
        depth = 1
        fields = ('id', 'name_en', 'name_de', 'floor_num', 'floor_name', 'fk_poi_category', 'icon')


class PoiCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoiCategory
        fields = ('cat_name', 'cat_name_en', 'cat_name_de', 'icon', 'fk_poi_icon', 'enabled')


class PoiSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poi
        depth = 2
        fields = ('id', 'name', 'name_de', 'floor_num', 'fk_poi_category')
