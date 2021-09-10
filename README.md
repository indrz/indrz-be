# INDRZ API (a.k.a the backend)
[Gitlab](https://gitlab.com/indrz/indrz-backend) hosts the main repo 
Mirror repo is at [Github](https://github.com/indrz/indrz-be)

----------------------

This is the [indrz](https://www.indrz.com) API backend code repository.  
documentation here [indrz Docs](https://gitlab.com/indrz/indrz-doc)


[![GitHub stars](https://img.shields.io/github/stars/indrz/indrz.svg?style=flat-square)](https://github.com/indrz/indrz/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/indrz/indrz.svg)](https://github.com/indrz/indrz/issues)
[![GitHub release](https://img.shields.io/github/release/indrz/indrz.svg)](https://github.com/indrz/indrz/releases)
[![license](https://img.shields.io/badge/license-AGPL-blue.svg?style=flat-square)](https://raw.githubusercontent.com/indrz/indrz/master/LICENSE)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/indrz/indrz.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=%5Bobject%20Object%5D)

## Quick Start Backend Setup
We are working on making the setup easier, with an all docker development
environmentment.  The production deployment aswell will be an all docker
deployment.


1. Visit `indrz/settings/`and copy the `example-env.env` file and save as `.env` file in root folder.
1. Get Docker `.env`  environment varialbles ready, located in the root folder
   allong with the `docker-compose.yml` :
1. Build all required Docker images
    ```
    make build
    ```
1. Run application
    ```
    make run
    ```
1. Run database setup that will create postgresql schemas and set db user search_path
    ```
    make setup_indrz_db
    ```
1. Load demo data for testing
    ```
    make load_demo_data
    ```
1. Collect static file
    ```
    make collectstatic
    ```
### Manage Postgres database
If you have issues with the db `setup_indrz_db`

```bash
psql -h localhost -U POSTGRES_USER -p POSTGRES_EXT_PORT -l
docker exec -it indrz_db bash
su postgres
dropdb indrzcloud
createdb -O indrzcloud indrzcloud
psql -c "create extension postgis" -d indrzcloud
psql -c "create extension pgrouting" -d indrzcloud
psql -c "CREATE SCHEMA IF NOT EXISTS django AUTHORIZATION indrzcloud" -d indrzcloud
psql -c "CREATE SCHEMA IF NOT EXISTS geodata AUTHORIZATION indrzcloud" -d indrzcloud
psql -c "ALTER ROLE indrzcloud IN DATABASE indrzcloud SET search_path TO django,geodata,public;" -d indrzcloud
```

### User Make command

Commands help

```
make
- or -
make help
```

Collect Django static files
```
make collectstatic
```

Build Docker images

```
# Build Indrz image only
make build-indrz

# Build all
make build
```

Stop application 
```
make stop
```

Application releases deployment 
```
make deploy
```

Pull code from Git 
```
make pull
```

## Tech

* [Python](https://python.org) (3.x)
* [Django](http://djangoproject.com) – Web Framework Backend
* [Django Rest Framework](http://www.django-rest-framework.org) – Django Rest Web Framework our API
* [PostGIS](http://postgis.net) – Spatial Database extension to Postgresql
* [PGRouting](http://pgrouting.org) - Routing extension to PostGIS and Posgresql
* [Postgresql](http://www.postgresql.org) – Database
* [Geoserver](http://geoserver.org) – Web map server to serve and create, maps and data
* [Ubuntu server](https://ubuntu.com/) - Server
* [Docker, docker-compose](https://docker.com/) - Docker, Docker-Compse

## Supported and built by:

Contact: Michael Diener

[www.gomogi.com](https://www.gomogi.com)


