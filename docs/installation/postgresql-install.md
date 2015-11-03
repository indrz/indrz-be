Postgresql Setup
================

```sql

CREATE ROLE indrz LOGIN ENCRYPTED PASSWORD 'bigsecret'
   VALID UNTIL 'infinity';

ALTER ROLE indrz SET search_path = django, public;

CREATE EXTENSION postgis;

CREATE EXTENSION pgrouting;

```