from django.utils.safestring import SafeString, mark_safe, SafeData
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Poi, PoiCategory, PoiIcon


class PoiSerializer(GeoFeatureModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Poi
        geo_field = 'geom'
        fields = '__all__'

    def get_icon(self, Poi):
        """

        :param Poi: poi obeject
        :return: a field ie property called icon for model Poi
        """
        if Poi.category:
            if Poi.category.fk_poi_icon:
                if Poi.category.fk_poi_icon.icon.url:
                    icon_url = Poi.category.fk_poi_icon.icon.url
                    if icon_url:
                        return icon_url
                    else:
                        return None
                else:
                    return None
            else:
                return None
        else:
            return None


class PoiCategorySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    html = serializers.SerializerMethodField()

    class Meta:
        model = PoiCategory
        fields = ('id', 'cat_name', 'cat_name_en', 'cat_name_de', 'icon', 'fk_poi_icon', 'enabled', 'html')

    def get_html(self, PoiCategory):
        return PoiCategory.html_content

        # return PoiCategory.html_field

    def get_icon(self, PoiCategory):
        request = self.context.get('request')
        if PoiCategory.fk_poi_icon:
            if PoiCategory.fk_poi_icon.icon and hasattr(PoiCategory.fk_poi_icon.icon, "url"):
                icon_url = PoiCategory.fk_poi_icon.icon.url
                if request:
                    return icon_url
                else:
                    return icon_url
            else:
                return None
        else:
            return None


class PoiIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoiIcon
        fields = ('id', 'name', 'icon')
