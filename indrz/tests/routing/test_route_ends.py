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

# Start Edge ################

nearest_start_node_id = 1770

nearest_start_edge_id = 3001
nearest_start_edge_source_id = 1770
nearest_start_edge_target_id = 1790

def substring(geom, fraction_from, fraction_to):
    pass


def test_source_nearest_node_equals_target():
    if nearest_start_node_id == nearest_start_edge_target_id:
        substring('geom', 0.8, 1) # 1 represents the end of the line
    pass


def test_source_nearest_node_equals_source():
    if nearest_start_node_id == nearest_start_edge_source_id:
        substring('geom', 0, 0.8) # 0 represents the start of the line
    pass


def test_both_nodes_from_nearest_edge_in_route_node_ids():
    pass


# End edge ##################

nearest_end_node_id = 1999

nearest_end_edge_id = 4000
nearest_end_edge_source_id = 8000
nearest_end_edge_target_id = 8100


#if both edge-node-ids in ids
#  then the route goes from xyz nearest-node to other edge-id
#else:
#  then the route goes from xyz to nearest node  NOT through other edge-id



