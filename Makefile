SHELL=/bin/bash
PWD ?= pwd_unknown

cnf ?= .env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: build-gse build-indrz build-geoserver build-nginx  ## Build all Docker images

build-gogse: ## Build Gomogi Geospatial Environment (GDAL, PROJ, GEOS)
	docker build -t gogse:latest -f devops/docker/gogse/Dockerfile

build-nginx: ## Build Nginx Image
	docker-compose build --build-arg ENV_TYPE=$(ENV_TYPE) --build-arg WEB_FOLDER=$(WEB_FOLDER) nginx

build-indrz: ## Build Indrz BE Image
	docker-compose build --build-arg ENV_TYPE=$(ENV_TYPE) indrz_be

build-geoserver: ## Build Geoserver Image
	docker-compose build geoserver

run: ## Run Indrz Docker project
	docker-compose -p $(PROJECT_NAME) up -d

collectstatic: ## Collect Django static files
	docker exec -t indrz python manage.py collectstatic --clear --noinput
	docker exec -t nginx cp -r /opt/data/static/dist/. $(WEB_FOLDER)/
	docker exec -t nginx cp -r /opt/data/static $(WEB_FOLDER)/

migrate:
	docker exec -t indrz python manage.py migrate

pull: ## Pull source code from Git
	git pull

deploy: pull migrate collectstatic run ## Update and deploy Indrz application
	docker restart indrz

stop: ## Stop Indrz Docker project
	docker-compose down