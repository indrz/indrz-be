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

build-api-dev: ## Build Indrz BE Image
	docker build -t indrz-os/api_dev:latest -f devops/docker/local/indrz_api/Dockerfile .

build-nginx-dev: ## Build Indrz BE Image
	docker build -t indrz-os/nginx_dev:latest -f devops/docker/local/nginx/Dockerfile .

build-fe-dev: ## Build Indrz BE Image
	docker build -t indrz-os/fe_dev:latest -f ../indrz-frontend/devops/docker/local/frontend/Dockerfile .

build-geoserver: ## Build Geoserver Image
	docker build -t indrz-os/geoserver_dev:latest -f devops/docker/local/geoserver/Dockerfile .

run: ## Run Indrz Docker project in development mode
	docker-compose -p indrz -f docker-compose-local.yml up -d

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
