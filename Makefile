SHELL=/bin/bash
PWD ?= pwd_unknown

cnf ?= .env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: build-nginx build-indrz ## Build Nginx and Indrz docker images

build-nginx: ## Build Nginx Image
	docker-compose build --build-arg ENV_TYPE=$(ENV_TYPE) --build-arg WEB_FOLDER=$(WEB_FOLDER) nginx

build-indrz: ## Build Indrz Image
	docker-compose build --build-arg ENV_TYPE=$(ENV_TYPE) indrz

run: ## Run Indrz Docker project
	docker-compose -p $(PROJECT_NAME) up -d

collectstatic: ## Collect Django static files
	docker exec -t indrz python manage.py collectstatic --clear --noinput
	docker exec -t nginx cp -r /opt/data/static/dist/. $(WEB_FOLDER)/
	docker exec -t nginx cp -r /opt/data/static $(WEB_FOLDER)/

pull: ## Pull source code from Git
	git pull

deploy: pull collectstatic run ## Update and deploy Indrz application

stop: ## Stop Indrz Docker project
	docker-compose down

