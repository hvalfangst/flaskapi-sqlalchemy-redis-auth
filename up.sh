#!/bin/sh

# Exits immediately if a command exits with a non-zero status
set -e

# Provision PostgresSQL, Redis and Flask API containers on the same network
docker-compose up -d --build;