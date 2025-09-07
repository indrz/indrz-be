SHELL=/bin/bash
PWD ?= pwd_unknown
PROJECT_NAME=indrz
COMPOSE_IGNORE_ORPHANS=True
BACKEND_NET=indrz-net

# cnf ?= indrz/settings/.env
# include $(cnf)
# export $(shell sed 's/=.*//' $(cnf))

.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build-fe-dev: ## Build indrz_web Docker Image
	docker build --progress plain --no-cache -t indrz-os/frontend_dev -f devops/docker/local/frontend/Dockerfile .