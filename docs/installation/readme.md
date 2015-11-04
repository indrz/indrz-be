Installation
============


Software and Technology
=======================

indrz is built on the shoulders of the following open source projects

Software      | License
------------- | -------------
PostgreSQL 9.3  | PostgreSQL License
Postgis 2.1     | GNU General Public License (GPLv2)
pgRouting 2.0   | GNU General Public License (GPLv2)
python 2.7.x    | PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
Django 1.8      | Django Software Foundation  a type BSD
GDAL            | MIT
Geoserver       | GNU General Public License (GPLv2), plus Apache 2.0
Openlayers 3.x  | 2-Clause BSD
jQuery          | MIT
Bootstrap       | MIT copyright 2015 Twitter



Requirements
============

  1. Postgresql 9.3.x
  1. PostGIS 2.1.x
  1. Python 2.7.x
  1. Django 1.8 (web framework) + other Django Apps(see requirements.txt)

Instructions
============

1. Install PostgreSQL 9.3, this I will leave up to you and some googleling
1. Install PostGIS Extension for your PostgreSQL install
1. Install Python 2.7.x
1. Install Django 1.8
1. Install all other python repos with pip
1. Check out the GIT repo and start


Windows users
=============

Create a python virtual environment
Download pyscopg2 windows binary http://www.stickpeople.com/projects/python/win-psycopg/index.2.5.4.html

Create python virtual env

enter virtual env

```bash
C:\> C:\virtualenv\Scripts\activate.bat 
(virtualenv) C:\> easy_install psycopg2-2.5.4.win32-py2.7-pg9.3.5-release.exe
```


Get the indrz GIT repostiory Started
====================================

[GIT how to fork indrz] (https://help.github.com/articles/fork-a-repo/)



