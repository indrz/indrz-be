FROM nginx:1.17
ARG ENV_TYPE
ARG WEB_FOLDER

RUN mkdir -p $WEB_FOLDER
COPY devops/docker/nginx/conf.d/allowed.conf /etc/nginx/allowed.conf
COPY devops/docker/nginx/conf.d/locations.conf /etc/nginx/locations.conf
COPY devops/docker/nginx/conf.d/default-$ENV_TYPE.conf /etc/nginx/conf.d/default.conf
