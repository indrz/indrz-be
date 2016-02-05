# Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2016 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2016 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# Copyright (C) 2014-2016 Anler Hernández <hello@anler.me>
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

from django.utils.translation import ugettext_lazy as _

ANON_PERMISSIONS = [
    ('view_organization', _('View organization')),
    ('view_map', _('View organization map')),

]

USER_PERMISSIONS = [
    ('view_organization', _('View organization')),
    ('view_map', _('View organization map')),
    ('request_membership', _('Request membership')),
    ('add_map_to_organization', _('Add map to organization')),
    ('add_comments_to_organization', _('Add comments to organization')),
    ('add_comments_to_map', _('Add comments to map')),
    ('modify_organization', _('Modify organization')),
    ('modify_map', _('Modify map')),
]

MEMBERS_PERMISSIONS = [
    ('view_organization', _('View organization')),
    # Map permissions
    ('view_map', _('View map ')),
    ('add_map', _('Add map ')),
    ('modify_map', _('Modify map map')),
    ('delete_map', _('Delete map map')),
    # layer permissions
    ('view_layer', _('View layer')),
    ('add_layer', _('Add layer')),
    ('modify_layer', _('Modify layer')),
    # building permissions
    ('view_building', _('View building')),
    ('add_building', _('Add building')),
    ('modify_building', _('Modify building')),

]

OWNERS_PERMISSIONS = [
    ('modify_organization', _('Modify organization')),
    ('add_member', _('Add member')),
    ('remove_member', _('Remove member')),
    ('delete_organization', _('Delete organization')),
    ('admin_organization_values', _('Admin organization values')),
    ('admin_roles', _('Admin roles')),
]
