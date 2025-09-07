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

from django.urls import re_path
from buildings.views import building_list, building_detail, \
    get_external_id, building_floors_list, get_floor_info, get_building_floor_spaces, \
    get_space_by_id, get_space_by_name

urlpatterns = [
    re_path(r'^$', building_list, name='list_buildings'),
    re_path(r'^(?P<pk>[0-9]+)/$', building_detail, name='building_details'),
    re_path(r'^(?P<building_id>\d{1,5})/externid/(?P<external_room_id>.+)/$', get_external_id, name='get_external_ids'),
    re_path(r'^(?P<building_id>\d{1,5})/floors/$', building_floors_list, name='get_floor_ids'),
    re_path(r'^(?P<building_id>\d{1,5})/floors/(?P<floor_id>\d{1,5})/$', get_floor_info, name='show_floor_info'),
    re_path(r'^(?P<building_id>\d{1,5})/floors/(?P<floor_id>\d{1,5})/spaces/$', get_building_floor_spaces, name='get_building_floor_spaces'),
    re_path(r'^(?P<building_id>\d{1,5})/floors/(?P<floor_id>\d{1,5})/spaces/(?P<space_id>\d{1,5})/$', get_space_by_id, name='show_space_by_id'),
    re_path(r'^(?P<building_id>\d{1,5})/floors/(?P<floor_id>\d{1,5})/spaces/(?P<space_name>.+)/$', get_space_by_name, name='show_space_by_name'),
]
