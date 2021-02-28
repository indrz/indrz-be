FROM nginx:1.18
ARG ENV_TYPE

RUN mkdir -p /var/www/indrz
COPY devops/docker/nginx/conf/allowed.conf /etc/nginx/allowed.conf
COPY devops/docker/nginx/conf/locations.conf /etc/nginx/locations.conf
COPY devops/docker/nginx/conf/default-$ENV_TYPE.conf /etc/nginx/conf.d/default.conf
