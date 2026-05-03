SHELL=/bin/bash

COMPOSE_FILE := docker-compose-local.yml
INIT_LOCKFILE := backend/indrz/.initialized

.PHONY: help ensure-data-dirs up up-api down down-api down-volumes migrate load-data-dev superuser fresh-install fresh-install-api-only

DATA_DIRS := \
	backend/data/cad \
	backend/data/logs \
	backend/data/media \
	backend/data/static \
	backend/data/temp_dwg \
	backend/data/src_dwg

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: build-indrz build-geoserver ## Build all Docker images

build-api-dev: ## Build Indrz BE Image
	docker build -t indrz-ee/api:3.1.4 -f devops/docker/local/indrz_api/Dockerfile .

build-nginx-dev: ## Build Indrz BE Image
	docker build -t indrz-ee/nginx:1.28.0 -f devops/docker/local/nginx/Dockerfile .

build-fe-dev: ## Build Indrz BE Image
	docker build -t indrz-ee/frontend:4.0.1 -f frontend/devops/docker/local/frontend/Dockerfile .

build-geoserver: ## Build Geoserver Image
	docker build -t indrz-ee/geoserver:2.28.2 -f devops/docker/local/geoserver/Dockerfile .

ensure-data-dirs: ## Ensure backend data folders exist for local bind mounts
	@mkdir -p $(DATA_DIRS)

up: ensure-data-dirs ## Run Indrz Docker project in development mode
	docker compose -f $(COMPOSE_FILE) up -d

up-api: ensure-data-dirs ## Run Indrz Docker project in development mode
	docker compose -f $(COMPOSE_FILE) up indrz_db indrz_api -d

down-api: ## Run Indrz Docker project in development mode
	docker compose -f $(COMPOSE_FILE) down indrz_db indrz_api

down: ## Stop Indrz Docker project
	docker compose -f $(COMPOSE_FILE) down

down-volumes: ## Stop local stack and remove named volumes (full DB reset)
	docker compose -f $(COMPOSE_FILE) down -v --remove-orphans
#	docker stop indrz_api nginx geoserver indrz_db frontend
#	docker rm indrz_api nginx geoserver indrz_db frontend

migrate: ## Migrate
	docker exec indrz_api python3 manage.py migrate --noinput
	docker exec indrz_api python3 manage.py collectstatic --noinput


load-data-dev: ## load data
	docker exec indrz_api python3 manage.py loaddata --app organizations organization.json
	docker exec indrz_api python3 manage.py loaddata --app campus campus.json
	docker exec indrz_api python3 manage.py loaddata --app buildings buildings.json
	docker exec indrz_api python3 manage.py loaddata --app buildings building_floors.json
	docker exec indrz_api python3 manage.py loaddata --app buildings initial_ltspacetype_data.json
	docker exec indrz_api python3 manage.py loaddata --app buildings building_spaces.json
	docker exec indrz_api python3 manage.py loaddata --app buildings building_wings.json
	docker exec indrz_api python3 manage.py loaddata --app poi_manager poi_icons.json
	docker exec indrz_api python3 manage.py loaddata --app poi_manager poi_categories.json
	docker exec indrz_api python3 manage.py loaddata --app poi_manager poi.json

superuser: ## Create superuser
	docker exec indrz_api python3 manage.py create_superuser

fresh-install: ensure-data-dirs ## Full local reset: drop DB, rerun init, and load dev fixtures
	docker compose -f $(COMPOSE_FILE) down -v --remove-orphans
	rm -f $(INIT_LOCKFILE)
	docker compose -f $(COMPOSE_FILE) up -d indrz_db
	@echo "Waiting for database healthcheck..."
	@for i in {1..90}; do \
		if [ "`docker inspect --format='{{.State.Health.Status}}' indrz_db 2>/dev/null`" = "healthy" ]; then \
			echo "Database is healthy"; \
			break; \
		fi; \
		sleep 2; \
		if [ $$i -eq 90 ]; then \
			echo "Timed out waiting for database to become healthy"; \
			exit 1; \
		fi; \
	done
	docker compose -f $(COMPOSE_FILE) up -d indrz_api
	@echo "Waiting for API initialization lock $(INIT_LOCKFILE)..."
	@for i in {1..90}; do \
		if [ -f "$(INIT_LOCKFILE)" ]; then \
			echo "API initialization complete"; \
			break; \
		fi; \
		sleep 2; \
		if [ $$i -eq 90 ]; then \
			echo "Timed out waiting for API initialization"; \
			exit 1; \
		fi; \
	done
	$(MAKE) load-data-dev
	docker compose -f $(COMPOSE_FILE) up -d

fresh-install-api-only: ensure-data-dirs ## Full local reset for DB+API only: drop DB, rerun init, and load dev fixtures
	docker compose -f $(COMPOSE_FILE) down -v --remove-orphans
	rm -f $(INIT_LOCKFILE)
	docker compose -f $(COMPOSE_FILE) up -d indrz_db
	@echo "Waiting for database healthcheck..."
	@for i in {1..90}; do \
		if [ "`docker inspect --format='{{.State.Health.Status}}' indrz_db 2>/dev/null`" = "healthy" ]; then \
			echo "Database is healthy"; \
			break; \
		fi; \
		sleep 2; \
		if [ $$i -eq 90 ]; then \
			echo "Timed out waiting for database to become healthy"; \
			exit 1; \
		fi; \
	done
	docker compose -f $(COMPOSE_FILE) up -d indrz_api
	@echo "Waiting for API initialization lock $(INIT_LOCKFILE)..."
	@for i in {1..90}; do \
		if [ -f "$(INIT_LOCKFILE)" ]; then \
			echo "API initialization complete"; \
			break; \
		fi; \
		sleep 2; \
		if [ $$i -eq 90 ]; then \
			echo "Timed out waiting for API initialization"; \
			exit 1; \
		fi; \
	done
	$(MAKE) load-data-dev
