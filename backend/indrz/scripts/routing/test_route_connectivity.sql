SELECT topology.CreateTopology('indrz_topo_eg', 31259);
SELECT topology.AddTopoGeometryColumn('indrz_topo_eg', 'routing', 'routing_networklines_eg', 'topo_geom', 'LINESTRING');

-- Layer 1, with 1.0 meter tolerance
UPDATE routing.routing_networklines_eg SET topo_geom = topology.toTopoGeom(geom, 'indrz_topo_eg', 1, 1.0);


-- use instead of update above if update above has errors this loop will skip errors and continue
DO $$DECLARE r record;
BEGIN
  FOR r IN SELECT * FROM routing.routing_networklines_eg LOOP
    BEGIN
      UPDATE routing.routing_networklines_eg SET topo_geom = topology.toTopoGeom(geom, 'indrz_topo_eg', 1, 0.01)
      WHERE id = r.id and r.network_type = 0;
    EXCEPTION
      WHEN OTHERS THEN
        RAISE WARNING 'Loading of record % failed: %', r.id, SQLERRM;
    END;
  END LOOP;
END$$;

-- split at intersections using topo network lines
SELECT r.id, r.floor_name, r.floor_num, r.network_type, e.geom
FROM indrz_topo_eg.edge e,
     indrz_topo_eg.relation rel,
     routing.routing_networklines_eg r
WHERE e.edge_id = rel.element_id
  AND rel.topogeo_id = (r.topo_geom).id;


-- lines not connected to network
SELECT id, st_length(geom), geom FROM routing.routing_networklines_eg_noded a
WHERE NOT EXISTS
 (SELECT 1 FROM routing.routing_networklines_eg_noded b
  WHERE a.id != b.id
  AND   ST_Intersects(a.geom, b.geom))


-- select ids of lower floor not connected to upper floor
-- ie ids from og01 stais, lifts not connected to og02 indoor floor 0
select a.id, a.geom from (select id, geom from geodata.routing_networklines_og01 where network_type in (1,2)) a
where a.id not in
(select distinct endline.id from geodata.routing_networklines_og01 endline
join geodata.routing_networklines_og02 startline
			on st_intersects(st_endpoint(endline.geom), st_startpoint(startline.geom))
			where endline.network_type in (1,2));