DROP FUNCTION route_fromAtoB(numeric, numeric, numeric, numeric, numeric, numeric);
CREATE OR REPLACE FUNCTION route_fromAtoB(
    IN x1 numeric, IN y1 numeric, IN z1 numeric,
    IN x2 numeric, IN y2 numeric, IN z2 numeric,
    OUT seq INTEGER,
    OUT gid BIGINT,
    OUT name TEXT,
    OUT length FLOAT,
    OUT the_time FLOAT,
    OUT azimuth FLOAT,
    OUT geom geometry
)
RETURNS SETOF record AS
$BODY$
DECLARE
    final_query TEXT;
BEGIN

    final_query :=
        FORMAT( $$
          WITH
            dijkstra AS (
                SELECT *
                FROM pgr_dijkstra(
                    'SELECT id, source, target, cost, reverse_cost FROM geodata.networklines_3857 WHERE 1=1',
                    -- source
                    (SELECT
                      verts.id as id
                      FROM geodata.networklines_3857_vertices_pgr AS verts
                      INNER JOIN
                        (select ST_PointFromText('POINT(%1$s %2$s %3$s)', 3857)as geom) AS pt
                      ON ST_DWithin(verts.the_geom, pt.geom, 50) and st_Z(verts.the_geom)=%3$s
                      ORDER BY ST_3DDistance(verts.the_geom, pt.geom)
                      LIMIT 1),
                    -- target
                    (SELECT
                      verts.id as id
                      FROM geodata.networklines_3857_vertices_pgr AS verts
                      INNER JOIN
                        (select ST_PointFromText('POINT(%4$s %5$s %6$s)', 3857)as geom) AS pt
                      ON ST_DWithin(verts.the_geom, pt.geom, 50) and st_Z(verts.the_geom)=%6$s
                      ORDER BY ST_3DDistance(verts.the_geom, pt.geom)
                      LIMIT 1)
                )
            ),
            get_geom AS (
                    SELECT dijkstra.*, input_network.network_type as network_type, input_network.id as id, input_network.floor as floor,
                        -- adjusting directionality
                        CASE
                            WHEN dijkstra.node = input_network.source THEN geom
                            ELSE ST_Reverse(geom)
                        END AS route_geom
                    FROM dijkstra JOIN geodata.networklines_3857 AS input_network ON (dijkstra.edge = input_network.id)
                    ORDER BY seq)
                SELECT seq, id, node, edge,
                    ST_Length(st_transform(route_geom,4326), TRUE ) AS cost,
                    agg_cost, floor, network_type,
                    ST_AsGeoJSON(route_geom) AS geoj,
                    degrees(ST_azimuth(ST_StartPoint(route_geom),
                    ST_EndPoint(route_geom))) AS azimuth,
                    route_geom
                FROM get_geom
                ORDER BY seq;$$,x1,y1,z1, x2,y2,z2); -- %1 to %5 of the FORMAT function
    RAISE notice '%', final_query;
    RETURN QUERY EXECUTE final_query;
END;
$BODY$
LANGUAGE 'plpgsql';

SELECT route_fromAtoB(1587929.168,5879642.328,3,1587963.046,5879655.956,3)

-- route_fromAtoB('SELECT id, source, target, cost, reverse_cost FROM geodata.networklines_3857 WHERE 1=1',x1,y1,z1,x2,y2,z2)

SELECT ST_AsGeoJSON(ST_LineSubstring('first_edge_geom', ST_LineLocatePoint('first_edge_geom', ST_SetSRID(ST_PointFromText(%2$s %3$s %4$s),3857)), 1));
SELECT ST_AsGeoJSON(ST_LineSubstring('last_edge_geom', 0, ST_LineLocatePoint('last_edge_geom', ST_SetSRID(ST_PointFromText(%5$s %6$s %7$s),3857))));


-- cut the line between two points
CREATE OR REPLACE FUNCTION cut_line_for_routing(schema character varying, geom_table character varying, geom_cname character varying, gid_cname character varying, gid int, source int, target int, start_point geometry, end_point geometry)
   RETURNS arbitraryRoute2 AS
$BODY$
DECLARE
    _r arbitraryRoute2;
    sql character varying;
    loc1 int;
    loc2 int;
BEGIN


    sql := 'SELECT (ST_Line_Substring_Advanced(' || quote_ident(geom_cname) || ',st_line_locate_point(' || quote_ident(geom_cname) || ', $1),'
            || ' st_line_locate_point(' || quote_ident(geom_cname) || ', $2))) as geom1, '
	    || ' (ST_Line_Substring_Advanced(' || quote_ident(geom_cname) || ',st_line_locate_point(' || quote_ident(geom_cname) || ', $2), '
            || ' st_line_locate_point(' || quote_ident(geom_cname) || ', $1))) as geom2, '
            || ' e.source as source, e.target as target, ' || quote_ident(gid_cname) || ' as gid, '
	    || ' (e.source = $3 OR e.source = $4) as direction FROM ' || quote_ident(geom_table) || ' e WHERE ' || quote_ident(gid_cname) || '=$5 ';

   -- RAISE NOTICE 'SQL: %', sql;
   -- RAISE NOTICE 'POINT: %', AsText(point);

    EXECUTE sql INTO _r USING start_point,end_point,source,target,gid;


    RETURN _r;

END;
$BODY$
  LANGUAGE 'plpgsql' VOLATILE STRICT
  COST 50;



CREATE OR REPLACE FUNCTION shortest_path_arbitrary_with_layer(schema character varying, geom_table character varying, geom_cname character varying, gid_cname character varying, cost_cname character varying, start_layer integer, end_layer integer, start_point_lon double precision, start_point_lat double precision, end_point_lon double precision, end_point_lat double precision)
  RETURNS setof arbitraryRouteLayer AS
$BODY$
DECLARE
    _r arbitraryRouteLayer;
    lastRec arbitraryRouteLayer;
    source_id int;
    target_id int;
    srid integer;
    start_point geometry;
    end_point geometry;
    start_rec SnapReturnType;
    end_rec SnapReturnType;
    innerSql character varying;
    sql character varying;
    cnt int;
    extraSQL character varying;
    extraRecord arbitraryRouteLayer2;
    tmpRecord arbitraryRouteLayer;
    start_rec_id int;
    end_rec_id int;
BEGIN
    srid := Find_SRID(quote_ident(schema),quote_ident(geom_table),quote_ident(geom_cname));

    start_point := SetSRID(GeomFromText('POINT(' || start_point_lon || ' ' || start_point_lat || ')'),srid);
    end_point   := SetSRID(GeomFromText('POINT(' || end_point_lon   || ' ' || end_point_lat   || ')'),srid);

    -- snapping to start_point
    -- RAISE NOTICE 'snap to start point: ';
    start_rec := snap_point_to_geom_on_layer(schema, geom_table, geom_cname, gid_cname, start_layer, start_point);
    -- snapping to end_point
    -- RAISE NOTICE 'snap to end point: ';
    end_rec   := snap_point_to_geom_on_layer(schema, geom_table, geom_cname, gid_cname, end_layer, end_point);


    -- check start_rec and end_rec location (= percentage of distance to start_rec.source)
    -- basically check whether the start location is closer to source or target of start_rec
    IF start_rec.location > 0.5 THEN
        start_rec_id = start_rec.target;
    ELSE
        start_rec_id = start_rec.source;
    END IF;

    -- check whether the end location is closer to source or target of end_rec
    IF end_rec.location > 0.5 THEN
        end_rec_id = end_rec.target;
    ELSE
        end_rec_id = end_rec.source;
    END IF;
    -- the points we just have chosen will be used for initializing shortest_path algorithm




    innerSql := 'SELECT ' || quote_ident(gid_cname) || ' AS id, source::int4, target::int4, ' || quote_ident(cost_cname) || '::double precision AS cost FROM ' || quote_ident(geom_table);

    -- routing
    sql := 'SELECT e.' || quote_ident(geom_cname) || ' as geom, e.source as source, e.target as target, e.' || quote_ident(gid_cname) || ' as gid, layer FROM '
		|| ' shortest_path_with_idx(''' || innerSql || ''','
		|| ' ' || start_rec_id || ', ' || end_rec_id || ', false, false) as t,  ' || quote_ident(geom_table) || ' as e WHERE e.' || quote_ident(gid_cname) || ' = t.edge_id AND '
                || ' e.' || quote_ident(gid_cname) || ' <> ' || start_rec.gid || ' AND e.' || quote_ident(gid_cname) || ' <> ' || end_rec.gid || ' ORDER BY t.idx';



--    RAISE NOTICE 'SQL: %', sql;

--    RAISE NOTICE 'Before loop';

    cnt := 0;

    FOR _r in EXECUTE sql
    LOOP
	-- in the very first step we need to add another line - the first line - to the output
	IF cnt = 0 THEN
		-- RAISE NOTICE 'in i=0: gid= %', _r.gid;

		extraRecord = cut_line_for_routing_layer(schema,geom_table,geom_cname,gid_cname,start_rec.gid,_r.source,_r.target,start_point);

		tmpRecord.source = extraRecord.source;
		tmpRecord.target = extraRecord.target;
		tmpRecord.gid    = extraRecord.gid;


		IF extraRecord.direction = 't' THEN
			tmpRecord.geom = Reverse(extraRecord.geom1);
		ELSE
			tmpRecord.geom = extraRecord.geom2;
		END IF;

		lastRec = tmpRecord;

		RETURN NEXT tmpRecord;
	END IF;



--        RAISE NOTICE 'Here %', _r.gid;
	IF _r.gid <> start_rec.gid AND _r.gid <> end_rec.gid THEN
		cnt = cnt + 1;

		IF lastRec.source = _r.source OR lastRec.target = _r.source THEN
			_r.geom = _r.geom;
		ELSE
			_r.geom = Reverse(_r.geom);
		END IF;


		lastRec = _r;
		RETURN NEXT _r;
	END IF;
    END LOOP;

 --   RAISE NOTICE 'after loop: gid= %', _r.gid;
 --   RAISE NOTICE 'cnt=%', cnt;

	IF cnt = 0 THEN
		IF start_rec.gid = end_rec.gid THEN
			-- this is if there is no rows in result, but there should be one (route is on the same linestring)
			extraRecord = cut_line_for_routing_layer(schema,geom_table,geom_cname,gid_cname,start_rec.gid,start_rec.source,start_rec.target,start_point,end_point);

			tmpRecord.source = extraRecord.source;
			tmpRecord.target = extraRecord.target;
			tmpRecord.gid    = extraRecord.gid;
			IF extraRecord.direction = 't' THEN
				tmpRecord.geom   = extraRecord.geom1;
			ELSE
				tmpRecord.geom   = Reverse(extraRecord.geom1);
			END IF;
			tmpRecord.layer  = extraRecord.layer;

			RETURN NEXT tmpRecord;
		ELSE
			-- this is when there is no rows in result, but there should be two (neighbours)

			IF start_rec.source = end_rec.source OR start_rec.source = end_rec.target THEN
				-- start linestring
				extraRecord = cut_line_for_routing_layer(schema,geom_table,geom_cname,gid_cname,start_rec.gid,start_rec.source,start_rec.target,start_point);
				tmpRecord.geom   = Reverse(extraRecord.geom1);
			ELSE

				-- start linestring
				extraRecord = cut_line_for_routing_layer(schema,geom_table,geom_cname,gid_cname,start_rec.gid,start_rec.source,start_rec.target,start_point);
				tmpRecord.geom   = extraRecord.geom2;
			END IF;

			tmpRecord.source = extraRecord.source;
			tmpRecord.target = extraRecord.target;
			tmpRecord.gid    = extraRecord.gid;
			tmpRecord.layer  = extraRecord.layer;

			RETURN NEXT tmpRecord;



			IF end_rec.source = start_rec.source OR end_rec.source = start_rec.target THEN
				-- target linestring
				extraRecord = cut_line_for_routing_layer(schema,geom_table,geom_cname,gid_cname,end_rec.gid,end_rec.source,end_rec.target,end_point);
				tmpRecord.geom   = extraRecord.geom1;
			ELSE

				-- target linestring
				extraRecord = cut_line_for_routing_layer(schema,geom_table,geom_cname,gid_cname,end_rec.gid,end_rec.source,end_rec.target,end_point);
				tmpRecord.geom   = Reverse(extraRecord.geom2);
			END IF;

			tmpRecord.source = extraRecord.source;
			tmpRecord.target = extraRecord.target;
			tmpRecord.gid    = extraRecord.gid;
			tmpRecord.layer  = extraRecord.layer;

			RETURN NEXT tmpRecord;

		END IF;
	ELSE
		-- this is the normal case
		extraRecord = cut_line_for_routing_layer(schema,geom_table,geom_cname,gid_cname,end_rec.gid,_r.source,_r.target,end_point);

		tmpRecord.source = extraRecord.source;
		tmpRecord.target = extraRecord.target;
		tmpRecord.gid    = extraRecord.gid;
		tmpRecord.layer  = extraRecord.layer;


		IF extraRecord.direction = 't' THEN
			tmpRecord.geom = extraRecord.geom1;
		ELSE
			tmpRecord.geom = Reverse(extraRecord.geom2);
		END IF;

		RETURN NEXT tmpRecord;

	END IF;


    RETURN;

END;
$BODY$
  LANGUAGE 'plpgsql' VOLATILE STRICT
  COST 600;

