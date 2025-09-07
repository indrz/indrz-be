CREATE SCHEMA IF NOT EXISTS django AUTHORIZATION indrz;
CREATE SCHEMA IF NOT EXISTS geodata AUTHORIZATION indrz;
ALTER ROLE indrz IN DATABASE indrz SET search_path TO django,geodata,dxf_tables,pre_django,bookway,routing,public;
