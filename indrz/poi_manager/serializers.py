# Copyright (C) 2014-2016 Michael Diener <m.diener@gomogi.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from rest_framework import serializers

from poi_manager.models import Poi, PoiCategory
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class PoiSerializer(GeoFeatureModelSerializer):


    class Meta:
        model = Poi
        geo_field = 'geom'
        depth = 1
        fields = ('id', 'name', 'floor_num', 'fk_poi_category')


class PoiCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoiCategory
        # fields = ('floor_num', 'short_name')