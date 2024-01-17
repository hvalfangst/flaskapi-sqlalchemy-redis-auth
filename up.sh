#!/bin/sh

# Exits immediately if a command exits with a non-zero status
set -e

docker-compose -f local/compose/db/docker-compose.yml up -d;
docker-compose -f local/compose/redis/docker-compose.yml up -d;
python python/main.py