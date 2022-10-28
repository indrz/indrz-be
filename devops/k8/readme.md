## Kubernetes Deployment Setup
This is the first attempt to document a kubernetes deployment using [Rancher deploying to Google Cloud Platform (GCP)](https://docs.ranchermanager.rancher.io/getting-started/quick-start-guides/deploy-rancher-manager/gcp).


## Components
1. Geoserver: serves our maptiles
1. Postgresql with PostGIS and PgRouting: stores our geospatial data and is the routing engine
1. Django + Django Restframework: our backend API in Python
1. Vuejs + Nuxtjs: the SPA frontend of indrz
1. Nginx: our webserver of choice to serve up our application

### Geoserver
Requires read/write access to
`/opt/geoserver/data_dir` where it stores all settings, configurations, `Tomcat`


### Postgresql
Requires persistant storage for the database folder


### Nginx

Urls to be served up
```
https://yourhost.com/api/v1/admin    Django API Admin
https://yourhost.com/api/v1    Django API Admin
https://yourhost.com/media    Django serve uploaded files such as POI icons
https://yourhost.com/static   Django Nginx serve static admin site js, css
https://yourhost.com/admin    Frontend Admin login
https://yourhost.com/geoserver  Geoserver admin login
https://yourhost.com/  Frontend application main site for our users ```


Gitlab registry   gitlab runner
