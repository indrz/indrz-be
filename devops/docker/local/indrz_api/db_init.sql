CREATE SCHEMA IF NOT EXISTS django AUTHORIZATION indrzcloud;
CREATE SCHEMA IF NOT EXISTS geodata AUTHORIZATION indrzcloud;
ALTER ROLE indrzcloud IN DATABASE indrzcloud SET search_path TO django,geodata;
