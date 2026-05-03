-- Meta-tables ------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS geodata.file_registry (
    path        text PRIMARY KEY,
    table_raw   text NOT NULL,
    mtime       timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS geodata.georef_params (
    table_raw       text PRIMARY KEY,
    x_org           double precision,
    y_org           double precision,
    x_geo           double precision,
    y_geo           double precision,
    scale           double precision default 1.0,
    rotate          double precision default 0.0, -- degrees
    updated_at      timestamptz default now(),
    geom_georef     geometry(Point, 4326)
    ;
-- helper function for upsert from Python
CREATE OR REPLACE FUNCTION _register_file(p_path text, p_mtime timestamptz, p_table text)
RETURNS void LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO file_registry(path, mtime, table_raw)
    VALUES(p_path, p_mtime, p_table)
    ON CONFLICT(path) DO UPDATE SET
        mtime = EXCLUDED.mtime,
        table_raw = EXCLUDED.table_raw;
END $$;
