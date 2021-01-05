# indrz backend
This is the [indrz](https://www.indrz.com) backend API code repository. You can find our documentation project here [indrz Docs](https://gitlab.com/indrz/indrz-doc) in the folder content


[![GitHub stars](https://img.shields.io/github/stars/indrz/indrz.svg?style=flat-square)](https://github.com/indrz/indrz/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/indrz/indrz.svg)](https://github.com/indrz/indrz/issues)
[![GitHub release](https://img.shields.io/github/release/indrz/indrz.svg)](https://github.com/indrz/indrz/releases)
[![license](https://img.shields.io/badge/license-AGPL-blue.svg?style=flat-square)](https://raw.githubusercontent.com/indrz/indrz/master/LICENSE)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/indrz/indrz.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=%5Bobject%20Object%5D)

## DevOps 

How to deploy and maintain application in all environments.

### Run the application (on local or remote env)

1. Create or copy project `.env` file in root folder.
2. Create or copy containers `*.env` files in `devops/docker-env` folder:
    1.  `db.env`
    2.  `db-backups.env`
    3.  `geoserver.env`
    4.  `indrz.env`
3. Include SSL Certificates in `ssl/` folder
4. Build all required Docker images
    ```
    make build
    ```
5. Run application
    ```
    make run
    ```
6. Collect static file
    ```
    make collectstatic
    ```

### Manage Postgres database

```
psql -h localhost -U POSTGRES_USER -p POSTGRES_EXT_PORT -l
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
# Build Nginx image only
make build-nginx

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

## Backend Tech

* Python 3.x
* [Django](http://djangoproject.com) – Web Framework Backend
* [Django Rest Framework](http://www.django-rest-framework.org) – Django Rest Web Framework our API
* [PostGIS](http://postgis.net) – Spatial Database extension to Postgresql
* [PGRouting](http://pgrouting.org) - Routing extension to PostGIS and Posgresql
* [Postgresql](http://www.postgresql.org) – Database
* [Geoserver](http://geoserver.org) – Web map server to serve and create, maps and data


## Supported and built by:

Contact: Michael Diener

Email: office@gomogi.com

[www.gomogi.com](https://www.gomogi.com)


