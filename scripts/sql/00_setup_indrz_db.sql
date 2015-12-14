CREATE ROLE "indrz-pg" LOGIN ENCRYPTED PASSWORD 'md539091991722381dcef6112d1b681b5d5'
  NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;


CREATE DATABASE indrz
  WITH OWNER = "indrz-pg"
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'German_Austria.1252'
       LC_CTYPE = 'German_Austria.1252'
       CONNECTION LIMIT = -1;

CREATE EXTENSION pgrouting
  SCHEMA public
  VERSION "2.0.0";

CREATE EXTENSION postgis
  SCHEMA public
  VERSION "2.1.7";

CREATE SCHEMA django AUTHORIZATION "indrz-pg";
CREATE SCHEMA geodata AUTHORIZATION "indrz-pg";


ALTER ROLE "indrz-pg"
  SET search_path = django, geodata, public;
