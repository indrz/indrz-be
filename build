#!/usr/bin/env bash
source ./.env

echo "Build Docker image for $ENV_TYPE env"

if [ "$1" == "nginx" ]; then
    docker-compose build --build-arg ENV_TYPE=$ENV_TYPE nginx
fi

if [ "$1" == "indrz" ]; then
    docker-compose build --build-arg ENV_TYPE=$ENV_TYPE indrz
fi