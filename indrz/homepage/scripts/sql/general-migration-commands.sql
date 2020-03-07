DELETE from bookway.all_sys_data;

SELECT id, regal_id, sys_von, sys_bis FROM bookway.shelfdata
WHERE sys_von = '16-0.0.1'
-- 12-0.2.2.Fisc.0
-- "16-275.10.10"
SELECT * FROM bookway.shelfdata WHERE sys_bis ILIKE '%16-0.30.%' OR sys_von ILIKE '%16-0.30.%';
SELECT * FROM bookway.shelfdata WHERE sys_von ILIKE '%12-KB%';

SELECT * FROM bookway.all_sys_data WHERE systemid ILIKE '%12-KB%';

SELECT * FROM bookway.shelfdata WHERE  stockwerk = 3 AND gebauede != 'Z';

UPDATE bookway.shelfdata SET floor_id = 41 WHERE stockwerk = 1 AND gebauede = 'Z';
UPDATE bookway.shelfdata SET floor_id = 35 WHERE stockwerk = 1 AND gebauede = 'W';

UPDATE bookway.shelfdata SET floor_id = 51 WHERE stockwerk = 2 AND gebauede = 'Z';
UPDATE bookway.shelfdata SET floor_id = 44 WHERE stockwerk = 2 AND gebauede = 'W';

UPDATE bookway.shelfdata SET floor_id = 57 WHERE stockwerk = 3 AND gebauede = 'Z';
UPDATE bookway.shelfdata SET floor_id = 54 WHERE stockwerk = 3 AND gebauede = 'W';

UPDATE bookway.shelfdata SET external_id = gebauede||stockwerk||sektion||regal_id;
UPDATE bookway.shelfdata SET sys_bis_array = regexp_split_to_array(sys_bis, '[-./:]');

select array_to_json(array_agg(row_to_json(t))) from (SELECT DISTINCT ON (name_de) name_de, id from django.poi_manager_poi ORDER BY name_de, id) as t ;


SELECT sys_von, sys_bis, sys_von_array, sys_bis_array FROM bookway.shelfdata WHERE sys_von_array > sys_bis_array;

SELECT external_id, sys_von, sys_bis
                FROM bookway.shelfdata
                WHERE sys_von_array >= ARRAY['16', '0', '30', 'Livi', '1']
                  AND sys_bis_array <= ARRAY['16', '0', '30', 'Livi', '1'];

INSERT INTO bookway.shelfdata (sys_von, sys_bis, sys_von_array, sys_bis_array) VALUES ('5-9.10', '5-10.1.0', '{5,9,10}', '{5,10,1,0}');
UPDATE bookway.shelfdata SET sys_von = '30-5', sys_bis = '30-11', sys_von_array = '{30,5}', sys_bis_array = '{30,11}';

UPDATE bookway.shelfdata SET sys_von_jsonb = to_json(sys_von_array), sys_bis_jsonb = to_json(sys_bis_array);


select array_to_json(array_agg(row_to_json(t))) from (SELECT sys_von, sys_bis from bookway.shelfdata ORDER BY sys_von) as t ;
SELECT sys_von, sys_bis, regexp_split_to_array(sys_von, '[-./:]') as von, regexp_split_to_array(sys_bis, '[-./:]') as bis from bookway.shelfdata;

SELECT to_json(sys_von_array ) from bookway.shelfdata;

SELECT DISTINCT short_name FROM django.buildings_buildingfloorspace ORDER BY short_name ASC ;

UPDATE django.buildings_buildingfloorspace SET space_type_id = 79 WHERE short_name like '%STGH%';

select array_to_json(array_agg(row_to_json(t))) from (SELECT DISTINCT ON (short_name) short_name, 94 as id from django.buildings_buildingfloorspace ORDER BY short_name, id) as t ;

SELECT DISTINCT category_id FROM django.poi_manager_poi ORDER BY category_id ASC ;


UPDATE django.poi_manager_poicategory set enabled = FALSE;


SELECT * FROM bookway.shelfdata WHERE sys_von_jsonb @> '["16", "0", "30"]';

SELECT * FROM bookway.shelfdata WHERE sys_von_jsonb ?& array['16', '0', '30'];


SELECT bs.id, ST_Buffer(bs.geom, (0.25)::double precision, 'endcap=flat'::text) AS geom
           FROM django.library_bookshelf as bs WHERE fk_building_floor_id = 51;

DROP VIEW geodata.e01_library_shelf_poly;
CREATE VIEW geodata.e01_library_shelf_poly AS SELECT DISTINCT ON (bs.id)
                     bs.id,
                     bs.external_id,
                     floor.floor_num,
                     shelfdata.sys_von,
                     shelfdata.sys_bis,
                     shelfdata.seite,
                     st_buffer(bs.geom, 0.25, 'endcap=square join=round') as geom
                    FROM
                     django.library_bookshelf as bs

                    LEFT JOIN django.buildings_buildingfloor as floor ON bs.fk_building_floor_id = floor.id
                    LEFT JOIN bookway.shelfdata as shelfdata ON bs.external_id = shelfdata.external_id
                    bs.external_id LIKE '%Z1%' OR bs.external_id LIKE '%W1%'
                    ORDER BY bs.id, bs.external_id, shelfdata.seite, shelfdata.measure_from;





  SELECT * FROM django.library_bookshelf WHERE external_id LIKE '%Z2%' OR external_id LIKE '%W2%'

SELECT bs.id, bs.external_id, bs.measure_from, bs.measure_to, sd.system_from, sd.system_to, sd.measure_from, sd.measure_to
  FROM django.library_bookshelf bs
    LEFT JOIN django.library_shelfdata as sd
      ON sd.external_shelf_id = bs.external_id
ORDER BY sd.system_from ASC ;


SELECT cast(system_from AS TEXT) AS label_from, external_shelf_id, shelf_side, system_from, system_to, measure_from, measure_to from django.library_shelfdata
WHERE external_shelf_id = 'Z3F14' AND measure_from = 0 AND shelf_side = 'L';

SELECT cast(system_from AS TEXT) AS label_from, external_shelf_id, shelf_side, system_from, system_to, measure_from, measure_to from django.library_shelfdata
WHERE external_shelf_id = 'Z3F14' AND measure_from = 0 AND shelf_side = 'R';

--get last value of
SELECT cast(system_from AS TEXT) as label_from, external_shelf_id, shelf_side, system_from, system_to, measure_from, measure_to from django.library_shelfdata
where external_shelf_id = 'Z3F1' AND measure_to = (SELECT max(measure_to) FROM django.library_shelfdata WHERE external_shelf_id = 'Z3F1')
OR external_shelf_id = 'Z3F1' AND measure_from = 0;

SELECT external_id, seite, sys_von, sys_bis, measure_from, measure_to from bookway.shelfdata
where external_id = 'Z3F1' AND measure_to = (SELECT max(measure_to) FROM django.library_shelfdata WHERE external_shelf_id = 'Z3F1')
OR external_id = 'Z3F1' AND measure_from < 1
ORDER BY measure_from;

select * from django.library_bookshelf WHERE substring(external_id, 4, 1) = 0;
