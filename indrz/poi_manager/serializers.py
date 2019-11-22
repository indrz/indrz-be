from rest_framework import serializers

from .models import Poi, PoiCategory
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class PoiSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Poi
        geo_field = 'geom'
        fields = '__all__'
        # depth = 1
        # fields = ('id', 'name', 'name_en', 'name_de', 'floor_num', 'floor_name', 'icon', )


class PoiCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoiCategory
        fields = ('cat_name', 'cat_name_en', 'cat_name_de', 'icon', 'fk_poi_icon', 'enabled')


class PoiSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poi
        depth = 2
        fields = ('id', 'name', 'name_de', 'floor_num', 'category')
