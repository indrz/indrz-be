from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Poi, PoiCategory, PoiIcon, PoiImages

class PoiSerializer(GeoFeatureModelSerializer):
    icon = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

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

    def get_images(self, Poi):
        """
        :param Poi: poi obeject
        :return: a field ie property called icon for model Poi
        """
        if PoiImages.objects.filter(poi_id=Poi.id):
            serializer = PoiImageSerializer(PoiImages.objects.filter(poi_id=Poi.id), many=True)
            return serializer.data
        else:
            return None

class PoiCategorySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    class Meta:
        model = PoiCategory
        fields = ('id', 'cat_name', 'cat_name_en', 'cat_name_de', 'icon', 'fk_poi_icon', 'enabled', 'parent')

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

class PoiImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    def get_image(self, PoiImages):

        request = self.context.get('request')
        if PoiImages.image and hasattr(PoiImages.image, "url"):
            image_url = PoiImages.image.url
            if request:
                return PoiImages.image.url
            return image_url

    def get_thumbnail(self, PoiImages):

        request = self.context.get('request')
        if PoiImages.thumbnail and hasattr(PoiImages.thumbnail, "url"):
            thumbnail_url = PoiImages.thumbnail.url
            if request:
                return PoiImages.thumbnail.url
            return thumbnail_url


    class Meta:
        model = PoiImages
        fields = ( 'id', 'poi', 'image', 'thumbnail', 'alt_text', 'sort_order', 'is_default')
