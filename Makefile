SHELL=/bin/bash
PWD ?= pwd_unknown

cnf ?= .env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: build-gogse build-indrz build-geoserver ## Build all Docker images

build-geodj: ## Build Gomogi Geospatial Environment (GDAL, PROJ, GEOS)
	docker build -t geodj:latest - < devops/docker/geodj/Dockerfile

build-indrz: ## Build Indrz BE Image
	docker-compose build --build-arg ENV_TYPE=$(ENV_TYPE) indrz_api

build-geoserver: ## Build Geoserver Image
	docker-compose build geoserver

run: ## Run Indrz Docker project (production-ready)
	docker-compose -p $(PROJECT_NAME) -f docker-compose.yml  up -d

run-dev: ## Run Indrz Docker project in development mode
	docker-compose -p $(PROJECT_NAME) -f docker-compose.dev.yml up -d

collectstatic: ## Collect Django static files
	docker exec -t indrz_api python3 manage.py collectstatic --clear --noinput
# 	docker exec -t nginx cp -r /opt/data/static/dist/. /var/www/indrz/
# 	docker exec -t nginx cp -r /opt/data/static /var/www/indrz/

setup_indrz_db:
	docker cp devops/docker/indrz/db_init.sql indrz_db:/scripts/db_init.sql
	docker exec -u postgres indrz_db psql indrzcloud postgres -f /scripts/db_init.sql

migrate:
	docker exec -t indrz_api python3 manage.py migrate

load_demo_data:
	docker exec -t indrz_api python3 manage.py loaddata fixture_buildings_organization.json
	docker exec -t indrz_api python3 manage.py loaddata fixture_buildings_campus.json
	docker exec -t indrz_api python3 manage.py loaddata fixture_buildings_building.json

pull: ## Pull source code from Git
	git pull

deploy: pull migrate collectstatic run ## Update and deploy Indrz application
	docker restart indrz_api

stop: ## Stop Indrz Docker project
	docker-compose down
