DROP VIEW geodata.e03_library_shelf_poly;
CREATE VIEW geodata.e03_library_shelf_poly AS SELECT DISTINCT ON (bs.id)
                     bs.id,
                     bs.external_id,
                     floor.floor_num,
                     shelfdata.sys_von,
                     shelfdata.sys_bis,
                     shelfdata.seite,
                     ST_Buffer(bs.geom, 0.25, 'endcap=flat join=round') as geom

                    FROM
                     django.library_bookshelf as bs

                    LEFT JOIN django.buildings_buildingfloor as floor ON bs.fk_building_floor_id = floor.id
                    LEFT JOIN bookway.shelfdata as shelfdata ON bs.external_id = shelfdata.external_id
                    WHERE bs.external_id LIKE 'Z3%' OR bs.external_id LIKE 'W3%'
                    ORDER BY bs.id, bs.external_id, shelfdata.seite, shelfdata.measure_from;

DROP VIEW geodata.e01_library_shelf_lines;
CREATE VIEW geodata.e01_library_shelf_lines AS SELECT DISTINCT ON (bs.id)
                     bs.id,
                     bs.external_id,
                     floor.floor_num,
                     shelfdata.sys_von,
                     shelfdata.sys_bis,
                     shelfdata.seite,
                     bs.geom as geom

                    FROM
                     django.library_bookshelf as bs

                    LEFT JOIN django.buildings_buildingfloor as floor ON bs.fk_building_floor_id = floor.id
                    LEFT JOIN bookway.shelfdata as shelfdata ON bs.external_id = shelfdata.external_id
                    WHERE bs.external_id LIKE 'Z1%' OR bs.external_id LIKE 'W1%'
                    ORDER BY bs.id, bs.external_id, shelfdata.seite, shelfdata.measure_from;

CREATE VIEW geodata.e02_library_shelf_lines AS SELECT DISTINCT ON (bs.id)
                     bs.id,
                     bs.external_id,
                     floor.floor_num,
                     shelfdata.sys_von,
                     shelfdata.sys_bis,
                     shelfdata.seite,
                     bs.geom as geom

                    FROM
                     django.library_bookshelf as bs

                    LEFT JOIN django.buildings_buildingfloor as floor ON bs.fk_building_floor_id = floor.id
                    LEFT JOIN bookway.shelfdata as shelfdata ON bs.external_id = shelfdata.external_id
                    WHERE bs.external_id LIKE 'Z2%' OR bs.external_id LIKE 'W2%'
                    ORDER BY bs.id, bs.external_id, shelfdata.seite, shelfdata.measure_from;

CREATE VIEW geodata.e03_library_shelf_lines AS SELECT DISTINCT ON (bs.id)
                     bs.id,
                     bs.external_id,
                     floor.floor_num,
                     shelfdata.sys_von,
                     shelfdata.sys_bis,
                     shelfdata.seite,
                     bs.geom as geom

                    FROM
                     django.library_bookshelf as bs

                    LEFT JOIN django.buildings_buildingfloor as floor ON bs.fk_building_floor_id = floor.id
                    LEFT JOIN bookway.shelfdata as shelfdata ON bs.external_id = shelfdata.external_id
                    WHERE bs.external_id LIKE 'Z3%' OR bs.external_id LIKE 'W3%'
                    ORDER BY bs.id, bs.external_id, shelfdata.seite, shelfdata.measure_from;