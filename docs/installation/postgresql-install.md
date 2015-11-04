Postgresql Setup
================

```sql
-- create a new user for your DB
CREATE ROLE indrz LOGIN ENCRYPTED PASSWORD 'bigsecret'
   VALID UNTIL 'infinity';
   
-- create a new schema to store all your tables
CREATE SCHEMA django AUTHORIZATION indrz;

-- set PostgreSQL search path to django so
-- when you install all your tables will
-- be created in the schema called django
-- this makes it easy to backup restore 

ALTER ROLE indrz SET search_path = django, public;

-- install postgis and pgrouting extensions
CREATE EXTENSION postgis;
CREATE EXTENSION pgrouting;

```