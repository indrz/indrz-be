# Use the official Nginx image as the base image
FROM nginx:1.22.1

# WORKDIR /var/www/indrz
WORKDIR /usr/share/nginx/html

# Copy the NGINX configuration file to the container
COPY devops/docker/local/nginx/conf/default-dev.conf /etc/nginx/conf.d/default.conf
