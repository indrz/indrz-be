SHELL=/bin/bash
PWD ?= pwd_unknown

cnf ?= indrz/settings/.env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: build-gogse build-indrz build-geoserver build-nginx  ## Build all Docker images

build-gogse: ## Build Gomogi Geospatial Environment (GDAL, PROJ, GEOS)
	docker build --build-arg GEOS_VERSION --build-arg PROJ_VERSION --build-arg GDAL_VERSION -t gogse:latest - < devops/docker/gogse/Dockerfile

build-nginx: ## Build Nginx Image
	docker-compose build --build-arg ENV_TYPE=$(ENV_TYPE) nginx

build-indrz: ## Build Indrz BE Image
	docker-compose build --build-arg ENV_TYPE=$(ENV_TYPE) indrz_api

build-geoserver: ## Build Geoserver Image
	docker-compose build geoserver

run: ## Run Indrz Docker project (production-ready)
	docker-compose -p $(PROJECT_NAME) up -d

run-dev: ## Run Indrz Docker project in development mode
	docker-compose -p $(PROJECT_NAME) -f docker-compose.yml -f docker-compose.dev.yml up -d

collectstatic: ## Collect Django static files
	docker exec -t indrz python manage.py collectstatic --clear --noinput
	docker exec -t nginx cp -r /opt/data/static/dist/. /var/www/indrz/
	docker exec -t nginx cp -r /opt/data/static /var/www/indrz/

migrate:
	docker exec -t indrz python manage.py migrate

pull: ## Pull source code from Git
	git pull

deploy: pull migrate collectstatic run ## Update and deploy Indrz application
	docker restart indrz

stop: ## Stop Indrz Docker project
	docker-compose down
