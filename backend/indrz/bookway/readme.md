# Bookway

## Core data fields (required)
*  shelf-id, external-shelf-id, shelf-side, from-rvk, to-rvk
*  shelf direction is not a data field but is required to define shelf-side (left or right).  Please use the map to ensure the shelf direction.  Visit ``/bookway/admin``

## Optional data fields
*  from-m, to-m, section-id

# Frontend Results options
1.  linestring: highlighted yellow line on the correct shelf side  ie  Left or Right
1.  point: the estimated point position based on from-m and to-m values if available