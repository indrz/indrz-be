--DROP VIEW geodata.search_index_v;
CREATE VIEW geodata.search_index_v AS SELECT landscape_landscapearea.id,
    landscape_landscapearea.name AS search_string,
    'landscapebuildings'::text AS text_type,
    ''::text AS external_id,
    0 AS layer,
    1 AS building_id,
    landscape_landscapearea.fk_campus_id AS campus_id,
    ST_Force2D(landscape_landscapearea.geom) AS geom,
    ''::text AS room_code
   FROM django.landscape_landscapearea
  WHERE (landscape_landscapearea.name IS NOT NULL)
UNION
 SELECT buildings_buildingfloorspace.id,
    buildings_buildingfloorspace.room_code AS search_string,
    'buildingfloorspace'::text AS text_type,
    buildings_buildingfloorspace.room_external_id AS external_id,
    buildings_buildingfloorspace.floor_num AS layer,
    buildings_buildingfloorspace.fk_building_id AS building_id,
    1 AS campus_id,
    ST_Force2D(buildings_buildingfloorspace.geom) AS geom,
    buildings_buildingfloorspace.room_code
   FROM django.buildings_buildingfloorspace
  WHERE (buildings_buildingfloorspace.room_code IS NOT NULL)
UNION
 SELECT buildings_buildingfloorspace.id,
    buildings_buildingfloorspace.room_external_id AS search_string,
    'aks'::text AS text_type,
    buildings_buildingfloorspace.room_external_id AS external_id,
    buildings_buildingfloorspace.floor_num AS layer,
    buildings_buildingfloorspace.fk_building_id AS building_id,
    1 AS campus_id,
    ST_Force2D(buildings_buildingfloorspace.geom) AS geom,
    buildings_buildingfloorspace.room_code
   FROM django.buildings_buildingfloorspace
  WHERE (buildings_buildingfloorspace.room_code IS NOT NULL)
UNION
 SELECT poi_manager_poi.id,
    poi_manager_poi.name AS search_string,
    'poi'::text AS text_type,
    ''::text AS external_id,
    poi_manager_poi.floor_num AS layer,
    poi_manager_poi.fk_building_id AS building_id,
    1 AS campus_id,
    ST_Force2D(poi_manager_poi.geom) AS geom,
    ''::text AS room_code
   FROM django.poi_manager_poi
  WHERE (poi_manager_poi.fk_poi_category_id <> 68 AND poi_manager_poi.enabled is TRUE )
UNION
 SELECT poi_manager_poi.id,
    poi_manager_poi.name_de AS search_string,
    'poi'::text AS text_type,
    ''::text AS external_id,
    poi_manager_poi.floor_num AS layer,
    poi_manager_poi.fk_building_id AS building_id,
    1 AS campus_id,
    ST_Force2D(poi_manager_poi.geom) AS geom,
    ''::text AS room_code
   FROM django.poi_manager_poi
  WHERE (poi_manager_poi.fk_poi_category_id <> 68 AND poi_manager_poi.enabled is TRUE );