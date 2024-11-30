
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

from django.conf.urls import url
from buildings.views import get_space_by_roomcode
from poi_manager.views import get_poi_by_id, get_poi_by_cat_id

urlpatterns = [
    url(r'poi/(?P<poi_id>[0-9]+)/$', get_poi_by_id, name='poi_share'),
    url(r'poi-category/(?P<cat_id>[0-9]+)/$', get_poi_by_cat_id, name='poi_share'),
    url(r'space/(?P<roomcode>.{5,12})/$', get_space_by_roomcode, name='space_share'),
]
