# Indrz-backend

**Requirements:**

- Docker
- Docker Compose

**Install**

- Clone the repo and `cd indrz-backend`
- Create `devops/docker-env/.env` file and set variables
- Create `indrz/settings/.env` file and set variables

        ```bash
        ########## docker ############
        PROJECT_NAME=indrz-backend
        ENV_TYPE=prod
        TIMEZONE=Europe/Vienna
        SSL_CERTIFICATES_PATH=./ssl
        WEB_FOLDER=/var/www

        ########## versions ############
        GEOS_VERSION=3.8.1
        PROJ_VERSION=6.3.2
        GDAL_VERSION=3.1.4

        ########## database ############
        POSTGRES_DB=indrz
        POSTGRES_USER=indrzguru
        POSTGRES_PASS=secretpassword
        POSTGRES_HOST=indrz_db
        POSTGRES_PORT=5432
        POSTGRES_EXT_PORT=5434

        ########## geoserver ############
        GEOSERVER_DATA_DIR=/opt/geoserver/data_dir
        ENABLE_JSONP=true
        MAX_FILTER_RULES=20
        OPTIMIZE_LINE_WIDTH=false
        FOOTPRINTS_DATA_DIR=/opt/footprints_dir
        GEOWEBCACHE_CACHE_DIR=/opt/geoserver/data_dir/gwc
        GEOSERVER_ADMIN_PASSWORD=yourSecretPWD9090
        INITIAL_MEMORY=2G
        MAXIMUM_MEMORY=4G
        GEOSERVER_EXT_PORT=8600

        ########## django ############
        SECRET_KEY='thissecret200needstobeeBIG8000LIKE999REALLYBIG2900'
        JS_DEBUG=True
        DEBUG=True
        STATIC_URL=/static/
        STATIC_ROOT=staticfiles
        STATIC_FOLDER=static
        MEDIA_URL=/media/
        MEDIA_ROOT=media
        INDRZ_API_TOKEN='Token 123abcYOURTOKENVALUEISHERE'
        LOCALHOST_URL='http://localhost:8000'
        ALLOWED_HOSTS=localhost
        SENTRY_URL=''
        LOGFILE_DIR=/logs/
        ```

- Install build packages

```bash
sudo apt-get install -y build-essentials
```

- Start builds

```bash
make build
[take a long time] 
```

- Run containers

```bash
make run
```

Running container output (`docker ps`):

```bash
CONTAINER ID   IMAGE                    COMMAND                  CREATED              STATUS                                 PORTS                                      NAMES
71dab676d029   indrz/nginx:latest       "/docker-entrypoint.…"   About a minute ago   Up About a minute                      0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp   nginx
ebe86ea2097c   indrz/geoserver:2.18.0   "/bin/sh /scripts/en…"   About a minute ago   Up About a minute (health: starting)   8443/tcp, 0.0.0.0:8600->8080/tcp           geoserver
6f26db9797fb   indrz/indrz-api:latest   "bash /entrypoint.sh…"   About a minute ago   Up About a minute                      0.0.0.0:8000->8000/tcp                     indrz_api
d8588c02d914   kartoza/postgis:13.0     "/bin/sh -c /scripts…"   About a minute ago   Up About a minute (healthy)            0.0.0.0:5434->5432/tcp                     indrz_db
```

- Access to **Indrz API** application from the browser:

`http://<IP ADDRESS>/api/`

## Troubleshooting

Bash / Terminal

```bash
# Check indrz_api logs, last 100 and follow
docker logs --tail=100 -f indrz_api

# Send a headers requestto API
curl -I http://0.0.0.0/api/
```

Error: **OPENSSL_1_1_1' not found (required by openssl) - [Building]**

Solution:

```bash
export LD_LIBRARY_PATH=/usr/local/lib
```

## Testing Machine

GCP IP: **35.241.139.208**

- Users

```bash
ssh mdiener@35.241.139.208
[password enabled]

# Super powers
sudo su
```

Projects root folder: `/opt/`

- `/opt/indrz-backend`
- `/opt/indrz-backend`

a copy of the password is stored in `/root/.pw`

Web page: [http://35.241.139.208/api/](http://35.241.139.208/api/)

## Issues

branch: `devops-docker-v2`

- Duplicated `.env` files
    - `devops/docker-env/.env`
    - `indrz/settings/.env`
- Sample env files must be updated

## Changelog

branch: `devops-docker-v2`

- Removed `sample.env` file from project root
- Removed `db_backups` from `docker-compose.yml`
- Removed all sample env files in `devops/docker-env` folder
- Fixed with nginx host header

```bash
Invalid HTTP_HOST header: 'indrz_api:8000'. The domain name provided is not valid according to RFC 1034/1035.
Bad Request: /api/
[13/Mar/2021 10:42:58] "HEAD /api/ HTTP/1.0" 400 64383
```
