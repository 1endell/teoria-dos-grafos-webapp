#! /bin/bash

docker compose down
docker image rm teoria-dos-grafos-webapp-front-end-grafos:latest
docker image rm teoria-dos-grafos-webapp-api-grafos:latest
git pull
docker compose up
