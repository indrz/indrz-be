#!/usr/bin/env bash
# Ubunut 14.04 trusty insall Postresql 9.5.1, PostGIS 2.2, PgRouting 2.1
# https://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS22UbuntuPGSQL95Apt

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt trusty-pgdg main" >> /etc/apt/sources.list'
wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update

# Install Postgresql 9.5, PostGIS
sudo apt-get install postgresql-9.5-postgis-2.2 pgadmin3 postgresql-contrib-9.5

# Install pgRouting 2.1 package 
sudo apt-get install postgresql-9.5-pgrouting