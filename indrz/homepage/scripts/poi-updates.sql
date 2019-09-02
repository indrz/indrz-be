SELECT name, description from django.poi_manager_poi ORDER BY name asc;

SELECT name, description from django.poi_manager_poi WHERE name like '%Dus%';

UPDATE django.poi_manager_poi set name = replace(name, 'Fahrradstellplatz überdacht', 'Bike parking covered');


SELECT replace(name, 'Veranstaltungsräume', 'Event Room') from django.poi_manager_poi ORDER BY name ASC ;