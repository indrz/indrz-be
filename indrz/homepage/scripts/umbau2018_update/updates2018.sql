select a.raumnr_tuer cad_raumnr, "RAUMNR", "RAUMNR_SCHILD", "RAUMNR_ALT" from temp.raumlist_data r
right join temp.e01_atts a ON upper(r."RAUMNR") = upper(a.raumnr_tuer)
order by "RAUMNR_SCHILD" desc;

ALTER TABLE temp.e00_spaces ADD room_code varchar(250) NULL;
ALTER TABLE temp.e01_spaces ADD room_code varchar(250) NULL;
ALTER TABLE temp.e02_spaces ADD room_code varchar(250) NULL;
ALTER TABLE temp.e03_spaces ADD room_code varchar(250) NULL;

ALTER TABLE temp.e00_spaces ADD room_num varchar(250) NULL;
ALTER TABLE temp.e01_spaces ADD room_num varchar(250) NULL;
ALTER TABLE temp.e02_spaces ADD room_num varchar(250) NULL;
ALTER TABLE temp.e03_spaces ADD room_num varchar(250) NULL;

ALTER TABLE temp.e00_spaces ADD building_id integer NULL;
ALTER TABLE temp.e01_spaces ADD building_id integer NULL;
ALTER TABLE temp.e02_spaces ADD building_id integer NULL;
ALTER TABLE temp.e03_spaces ADD building_id integer NULL;

ALTER TABLE temp.e00_spaces ADD floor_id integer NULL;
ALTER TABLE temp.e01_spaces ADD floor_id integer NULL;
ALTER TABLE temp.e02_spaces ADD floor_id integer NULL;
ALTER TABLE temp.e03_spaces ADD floor_id integer NULL;

ALTER TABLE temp.e00_spaces ADD space_type_id integer NULL;
ALTER TABLE temp.e01_spaces ADD space_type_id integer NULL;
ALTER TABLE temp.e02_spaces ADD space_type_id integer NULL;
ALTER TABLE temp.e03_spaces ADD space_type_id integer NULL;

ALTER TABLE temp.e00_spaces RENAME COLUMN building_id TO fk_building_id;
ALTER TABLE temp.e01_spaces RENAME COLUMN building_id TO fk_building_id;
ALTER TABLE temp.e02_spaces RENAME COLUMN building_id TO fk_building_id;
ALTER TABLE temp.e03_spaces RENAME COLUMN building_id TO fk_building_id;

ALTER TABLE temp.e00_spaces RENAME COLUMN floor_id TO fk_building_floor_id;
ALTER TABLE temp.e01_spaces RENAME COLUMN floor_id TO fk_building_floor_id;
ALTER TABLE temp.e02_spaces RENAME COLUMN floor_id TO fk_building_floor_id;
ALTER TABLE temp.e03_spaces RENAME COLUMN floor_id TO fk_building_floor_id;

ALTER TABLE temp.e00_spaces ADD geom2d geometry(MultiPolygon,3857) NULL;
update temp.e00_spaces set geom2d = ST_Force2d(geom);
ALTER TABLE temp.e01_spaces ADD geom2d geometry(MultiPolygon,3857) NULL;
update temp.e01_spaces set geom2d = ST_Force2d(geom);
ALTER TABLE temp.e02_spaces ADD geom2d geometry(MultiPolygon,3857) NULL;
update temp.e02_spaces set geom2d = ST_Force2d(geom);
ALTER TABLE temp.e03_spaces ADD geom2d geometry(MultiPolygon,3857) NULL;
update temp.e03_spaces set geom2d = ST_Force2d(geom);

update temp.e00_spaces as s set room_num = a.raumnr_tuer from temp.e00_atts as a
     where ST_Within(a.geom, s.geom);
update temp.e01_spaces as s set room_num = a.raumnr_tuer from temp.e01_atts as a
     where ST_Within(a.geom, s.geom);
update temp.e02_spaces as s set room_num = a.raumnr_tuer from temp.e02_atts as a
     where ST_Within(a.geom, s.geom);
update temp.e03_spaces as s set room_num = a.raumnr_tuer from temp.e03_atts as a
     where ST_Within(a.geom, s.geom);

update temp.e00_spaces as s set room_code = r."RAUMNR_SCHILD" from temp.raumlist_data as r
     where upper(r."RAUMNR") = upper(s.room_num)
update temp.e01_spaces as s set room_code = r."RAUMNR_SCHILD" from temp.raumlist_data as r
     where upper(r."RAUMNR") = upper(s.room_num)
update temp.e02_spaces as s set room_code = r."RAUMNR_SCHILD" from temp.raumlist_data as r
     where upper(r."RAUMNR") = upper(s.room_num)
update temp.e03_spaces as s set room_code = r."RAUMNR_SCHILD" from temp.raumlist_data as r
     where upper(r."RAUMNR") = upper(s.room_num)

update temp.e00_spaces as s set building_id = f.building_id from temp.e00_floor as f
     where ST_Within(s.geom, f.geom);
update temp.e01_spaces as s set room_num = a.raumnr_tuer from temp.e01_atts as a
     where ST_Within(a.geom, s.geom);
update temp.e02_spaces as s set room_num = a.raumnr_tuer from temp.e02_atts as a
     where ST_Within(a.geom, s.geom);
update temp.e03_spaces as s set room_num = a.raumnr_tuer from temp.e03_atts as a
     where ST_Within(a.geom, s.geom);

Delete from django.buildings_buildingfloor where id in (1,2,4,5,28,59)
Delete from django.buildings_buildingfloor where id in (1,2,4,5,28,59);


-- 25.10.2018
-- update geometry of all floor areas based on a 0,5m buffer of all new spaces e00
UPDATE django.buildings_buildingfloor set geom = (select st_multi(geom) from temp.e00_floor where id = 6) where id = 5
UPDATE django.buildings_buildingfloor set geom = (select st_multi(geom) from temp.e00_floor where id = 5) where id = 28
UPDATE django.buildings_buildingfloor set geom = (select st_multi(geom) from temp.e00_floor where id = 2) where id = 4 -- biblio
UPDATE django.buildings_buildingfloor set geom = (select st_multi(geom) from temp.e00_floor where id = 4) where id = 2
UPDATE django.buildings_buildingfloor set geom = (select st_multi(geom) from temp.e00_floor where id = 1) where id = 1


update temp.e00_spaces as s set fk_building_floor_id = f.id from django.buildings_buildingfloor as f
     where f.floor_num = 0 AND ST_Within(s.geom2d, f.geom);
update temp.e01_spaces as s set fk_building_floor_id = f.id from django.buildings_buildingfloor as f
     where f.floor_num = 1 AND ST_Within(s.geom, f.geom);
update temp.e02_spaces as s set fk_building_floor_id = f.id from django.buildings_buildingfloor as f
     where f.floor_num = 2 AND ST_Within(s.geom, f.geom);
update temp.e03_spaces as s set fk_building_floor_id = f.id from django.buildings_buildingfloor as f
     where f.floor_num = 3 AND ST_Within(s.geom, f.geom);

select s.room_code, s.room_number_sign, s.room_number, s.room_external_id, a.raumnr, a.raumnr_schild from geodata.aaudata as a, django.buildings_buildingfloorspace as s
where a.raumnr_schild = s.room_number_sign and s.fk_building_id = 12 order by s.room_code

select raumnr, raumnr_alt, raumnr_schild from geodata.aaudata where raumnr_schild like '%B10%' order by raumnr_schild;

select id, short_name, room_code, replace(room_code, 'L10.1.0', 'L10.1.') from buildings_buildingfloorspace where fk_building_id =12
order by room_code; --22(b01) 9(b02) 10(b04) 23(b07) 24(b08)  11 (b09) 12(b10)


select id, short_name, room_code, room_number, room_number_sign from buildings_buildingfloorspace where fk_building_id=12 order by room_code

update buildings_buildingfloorspace as s
  set room_code = a.raumnr_schild from geodata.aaudata as a
    where a.raumnr_schild = s.room_number_sign;

update buildings_buildingfloorspace as s
  set room_number = a.raumnr from geodata.aaudata as a
    where a.raumnr_schild = s.room_number_sign;

update buildings_buildingfloorspace
  set room_code = replace(room_code, 'L10.2.0.', 'L10.2.')
  where fk_building_id = 12;

update buildings_buildingfloorspace
  set room_code = replace(room_code, 'L10.0.0', 'L10.0.')
  where fk_building_id = 12;

update buildings_buildingfloorspace
  set room_code = replace(room_code, 'L10.1.0', 'L10.1.')
  where fk_building_id = 12;


update buildings_buildingfloorspace
  set room_code = replace(room_code, '7.1.', 'L7.1.')
  where fk_building_id = 23;

update buildings_buildingfloorspace
  set room_code = replace(room_code, '8.2.', 'L8.2.')
  where fk_building_id = 24;

select short_name, room_code, room_number, room_number_sign
  from buildings_buildingfloorspace
  where room_code is not null
    and room_number is null