from rest_framework import serializers
from rest_framework.fields import CharField

from .models import Poi, PoiCategory

from rest_framework_gis.serializers import GeoFeatureModelSerializer


class PoiSerializer(GeoFeatureModelSerializer):
    category_name = CharField(source='category.cat_name', read_only=True)
    category_name_de = CharField(source='category.cat_name_de', read_only=True)
    category_name_en = CharField(source='category.cat_name_en', read_only=True)
    category_icon = CharField(source='category.icon', read_only=True)
    category_icon_css_name = CharField(source='category.icon_css_name', read_only=True)

    class Meta:
        model = Poi
        geo_field = 'geom'
        # fields = '__all__'
        # depth = 1
        fields = ('id', 'name', 'name_en', 'name_de', 'enabled', 'floor_num', 'floor_name', 'icon', 'category',
                  'category_name', 'category_icon', 'category_name_en', 'category_name_de', 'category_icon_css_name')


class PoiCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoiCategory
        fields = ('id', 'cat_name', 'cat_name_en', 'cat_name_de', 'icon', 'fk_poi_icon', 'enabled')


class PoiSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poi
        depth = 2
        fields = ('id', 'name', 'name_de', 'floor_num', 'category')
