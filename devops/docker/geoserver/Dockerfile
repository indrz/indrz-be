FROM kartoza/geoserver:2.15.0

COPY devops/docker/geoserver/fonts/ /usr/share/fonts/truetype/
COPY devops/docker/geoserver/icons/ /opt/geoserver/data_dir/workspaces/indrztu/styles/
COPY devops/docker/geoserver/cors-web.xml /usr/local/tomcat/webapps/geoserver/WEB-INF/web.xml
