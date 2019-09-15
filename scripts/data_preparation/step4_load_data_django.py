import os
from django.contrib.gis.gdal import DataSource, SpatialReference
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry, LineString, Point, Polygon


import psycopg2
from pathlib import Path
from .utils import unique_floor_names, con_string

conn = psycopg2.connect(con_string)
cur = conn.cursor()


insert_spaces = f"""INSERT INTO django.buildings_buildingfloor (geom, short_name, floor_num, fk_building_id)
SELECT st_transform(geom, 3857) as geom, building, 0, 3
FROM geodata.eg00_umriss
WHERE geodata.eg00_umriss.building = 'AD';"""
