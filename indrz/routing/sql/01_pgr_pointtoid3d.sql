-- Function: public.pgr_pointtoid3d(geometry, double precision, text, integer)

-- DROP FUNCTION public.pgr_pointtoid3d(geometry, double precision, text, integer);

CREATE OR REPLACE FUNCTION public.pgr_pointtoid3d(point geometry, tolerance double precision, vertname text, srid integer)
  RETURNS bigint AS
$BODY$
DECLARE
    rec record;
    pid bigint;

BEGIN
    execute 'SELECT ST_3DDistance(the_geom,ST_GeomFromText(st_astext('||quote_literal(point::text)||'),'||srid||')) AS d, id, the_geom
        FROM '||pgr_quote_ident(vertname)||'
        WHERE ST_DWithin(the_geom, ST_GeomFromText(st_astext('||quote_literal(point::text)||'),'||srid||'),'|| tolerance||')
        ORDER BY d
        LIMIT 1' INTO rec ;
    IF rec.id is not null THEN
        pid := rec.id;
    ELSE
        execute 'INSERT INTO '||pgr_quote_ident(vertname)||' (the_geom) VALUES ('||quote_literal(point::text)||')';
        pid := lastval();
    END IF;

    RETURN pid;

END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION public.pgr_pointtoid3d(geometry, double precision, text, integer)
  OWNER TO postgres;
COMMENT ON FUNCTION public.pgr_pointtoid3d(geometry, double precision, text, integer) IS 'args: point geometry,tolerance,verticesTable,srid - inserts the point into the vertices table using tolerance to determine if its an existing point and returns the id assigned to it';



-- FUNCTION: public.pgr_pointtoid3d(geometry, double precision, text, integer, double precision)

-- DROP FUNCTION public.pgr_pointtoid3d(geometry, double precision, text, integer, double precision);

CREATE OR REPLACE FUNCTION public.pgr_pointtoid3d(
	point geometry,
	tolerance double precision,
	vertname text,
	srid integer,
	zlev double precision)
    RETURNS bigint
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE STRICT
AS $BODY$
DECLARE
    rec record;
    pid bigint;
    pnt geometry;

BEGIN
      pnt := st_translate(st_force_3d(point), 0.0, 0.0, coalesce(zlev :: FLOAT, 0.0));
--     execute 'SELECT ST_3DDistance(the_geom,ST_GeomFromText(st_astext('||quote_literal(point::text)||'),'||srid||')) AS d, id, the_geom
--         FROM '||pgr_quote_ident(vertname)||'
--         WHERE ST_DWithin(the_geom, ST_GeomFromText(st_astext('||quote_literal(point::text)||'),'||srid||'),'|| tolerance||')
--         ORDER BY d
--         LIMIT 1' INTO rec ;

      EXECUTE
      'SELECT
        id,
        the_geom
      FROM
        ' || vertname || '
      WHERE
        ST_expand(ST_GeomFromText(st_astext(' || quote_literal(pnt :: TEXT) || '),' || srid || '), ' || text(tolerance) || ') && the_geom AND
        ST_3DLength(ST_makeline(the_geom, ST_GeomFromText(st_astext(' || quote_literal(pnt :: TEXT) || '),' || srid ||
      '))) < ' || text(tolerance) || ' ORDER BY ST_3DLength(ST_makeline(the_geom, ST_GeomFromText(st_astext(' ||
      quote_literal(pnt :: TEXT) || '),' || srid ||
      '))) LIMIT 1'
      INTO rec;

    IF rec.id is not null THEN
        pid := rec.id;
    ELSE
        execute 'INSERT INTO '||pgr_quote_ident(vertname)||' (the_geom) VALUES ('||quote_literal(pnt::text)||')';
        pid := lastval();
    END IF;

    RETURN pid;

END;
$BODY$;

ALTER FUNCTION public.pgr_pointtoid3d(geometry, double precision, text, integer, double precision)
    OWNER TO postgres;

COMMENT ON FUNCTION public.pgr_pointtoid3d(geometry, double precision, text, integer, double precision)
    IS 'args: point geometry,tolerance,verticesTable,srid,zlev - inserts the point into the vertices table using tolerance to determine if its an existing point and returns the id assigned to it';
