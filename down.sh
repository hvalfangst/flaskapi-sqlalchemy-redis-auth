#!/bin/sh

# Exits immediately if a command exits with a non-zero status
set -e

docker-compose -f local/compose/db/docker-compose.yml down;
docker-compose -f local/compose/redis/docker-compose.yml down;