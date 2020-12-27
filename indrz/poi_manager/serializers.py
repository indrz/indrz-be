from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Poi, PoiCategory


class PoiSerializer(GeoFeatureModelSerializer):
    category_name = CharField(source='category.cat_name', read_only=True)
    category_name_de = CharField(source='category.cat_name_de', read_only=True)
    category_name_en = CharField(source='category.cat_name_en', read_only=True)
    category_icon_css_name = CharField(source='category.icon_css_name', read_only=True )
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Poi
        geo_field = 'geom'
        fields = ('id', 'name', 'name_en', 'name_de', 'enabled', 'floor_num', 'floor_name', 'icon', 'category',
                  'category_name', 'category_name_en', 'category_name_de', 'category_icon_css_name')

    def get_icon(self, Poi):
        """

        :param Poi: poi obeject
        :return: a field ie property called icon for model Poi
        """
        request = self.context.get('request')
        if Poi.category:
            if Poi.category.fk_poi_icon:
                if Poi.category.fk_poi_icon.icon.url:
                    icon_url = Poi.category.fk_poi_icon.icon.url
                    if request:
                        return request.build_absolute_uri(icon_url)
                    else:
                        return settings.LOCALHOST_URL + icon_url
                else:
                    return None
            else:
                return None
        else:
            return None

class PoiCategorySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    class Meta:
        model = PoiCategory
        fields = ('id', 'cat_name', 'cat_name_en', 'cat_name_de', 'icon', 'fk_poi_icon', 'enabled')

    def get_icon(self, PoiCategory):
        request = self.context.get('request')
        if PoiCategory.fk_poi_icon:
            if PoiCategory.fk_poi_icon.icon and hasattr(PoiCategory.fk_poi_icon.icon, "url"):
                icon_url = PoiCategory.fk_poi_icon.icon.url
                if request:
                    return request.build_absolute_uri(icon_url)
                else:
                    return settings.LOCALHOST_URL + icon_url
            else:
                return None
        else:
            return None

class PoiSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poi
        depth = 2
        fields = ('id', 'name', 'name_de', 'floor_num', 'category')
