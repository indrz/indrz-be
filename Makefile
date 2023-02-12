SHELL=/bin/bash
PWD ?= pwd_unknown

cnf ?= .env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: build-indrz build-geoserver ## Build all Docker images

build-indrz-api-prod: ## Build Indrz BE Image
	docker build -t indrz_api_prod:latest -f devops/docker/production/indrz_api/Dockerfile ./indrz

build-indrz-api-dev: ## Build Indrz BE Image
	docker build -t indrz_api_dev:latest -f devops/docker/local/indrz_api/Dockerfile ./indrz

build-geoserver: ## Build Geoserver Image
	docker-compose build geoserver

run: ## Run Indrz Docker project (production-ready)
	docker-compose -p $(PROJECT_NAME) -f docker-compose.yml  up -d

run-dev: ## Run Indrz Docker project in development mode
	docker-compose -p $(PROJECT_NAME) -f docker-compose-local.yml up -d

setup_indrz_db:
	docker cp devops/docker/indrz/db_init.sql indrz_db:/scripts/db_init.sql
	docker exec -u postgres indrz_db psql indrzcloud postgres -f /scripts/db_init.sql

migrate:
	docker exec -t indrz_api python3 manage.py migrate

load_demo_data_dev:
#	docker exec -t indrz_api python3 manage.py loaddata --app buildings organization.json
#	docker exec -t indrz_api python3 manage.py loaddata --app buildings campus.json
#	docker exec -t indrz_api python3 manage.py loaddata --app buildings buildings.json
#	docker exec -t indrz_api python3 manage.py loaddata --app buildings buildings_floors.json
#	docker exec -t indrz_api python3 manage.py loaddata --app buildings buildings_spaces.json
#	docker exec -t indrz_api python3 manage.py loaddata --app buildings buildings_wings.json
	docker exec -t indrz_api python3 manage.py loaddata --app buildings initial_ltspacetype_data.json


pull: ## Pull source code from Git
	git pull

deploy: pull migrate collectstatic run ## Update and deploy Indrz application
	docker restart indrz_api

stop: ## Stop Indrz Docker project
	docker-compose down
