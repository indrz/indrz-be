FROM nginx:1.22.1

ARG ENV_TYPE
ARG WEB_FOLDER

# WORKDIR /var/www/indrz
WORKDIR /usr/share/nginx/html

COPY devops/docker/local/nginx/conf/default-dev.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]
